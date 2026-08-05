# giscus setup

The repository and category IDs are already prepared in `mkdocs.yml`. One owner
action is still required:

1. Open <https://github.com/apps/giscus> while signed in as the repository owner.
2. Choose **Install** and grant access only to `forex-toolkit`.
3. Confirm GitHub Discussions is enabled for the repository.
4. Uncomment the `extra.giscus` block in `mkdocs.yml`.
5. Run `mkdocs build --strict`, open a page and post one test comment.

Prepared values:

```yaml
giscus:
  repo: MukhammadAmir-Akbarov/forex-toolkit
  repo_id: R_kgDOSi9ouA
  category: Announcements
  category_id: DIC_kwDOSi9ouM4C9qBu
```

Do not enable the block before the app is installed: the embedded widget would
only show an installation error to readers.
