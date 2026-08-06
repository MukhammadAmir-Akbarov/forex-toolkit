(function () {
  "use strict";

  var KEY = "forex_training_queue_v1";

  function read() {
    try {
      var value = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(value) ? value : [];
    } catch (error) {
      return [];
    }
  }

  function write(tasks) {
    try { localStorage.setItem(KEY, JSON.stringify(tasks.slice(0, 20))); } catch (error) {}
    return tasks;
  }

  function ensure(tasks, spec) {
    if (tasks.some(function (task) { return task.id === spec.id; })) return;
    tasks.push({
      id: spec.id,
      type: spec.type,
      category: spec.category || "",
      progress: 0,
      target: 10,
      createdAt: new Date().toISOString(),
      completedAt: null
    });
  }

  function sync(plans, replayStats) {
    var tasks = read();
    (plans || []).forEach(function (plan) {
      if (plan.status !== "closed") return;
      if (plan.moved_stop) ensure(tasks, { id: "stop-discipline", type: "stop" });
      if (String(plan.emotion || "").toLowerCase() === "fomo") {
        ensure(tasks, { id: "fomo-pause", type: "fomo" });
      }
      if (plan.followed_rules === false) ensure(tasks, { id: "rules-process", type: "rules" });
    });
    if (replayStats && replayStats.weakCategory) {
      ensure(tasks, {
        id: "structure-" + replayStats.weakCategory,
        type: "structure",
        category: replayStats.weakCategory
      });
    }
    return write(tasks);
  }

  function active() {
    return read().find(function (task) { return task.progress < task.target; }) || null;
  }

  function qualifies(task, action, category) {
    if (task.type === "fomo") return action === "skip";
    if (task.type === "structure") return action !== "skip" && task.category === category;
    return action !== "skip";
  }

  function advance(action, category) {
    var tasks = read();
    var task = tasks.find(function (item) { return item.progress < item.target; });
    if (!task || !qualifies(task, action, category)) return task || null;
    task.progress = Math.min(task.target, task.progress + 1);
    if (task.progress >= task.target) task.completedAt = new Date().toISOString();
    write(tasks);
    if (task.completedAt && window.fxTrack) {
      window.fxTrack("training_task_completed", { once: false });
    }
    return task;
  }

  window.FXTrainingQueue = { key: KEY, read: read, sync: sync, active: active, advance: advance };
})();
