# Agent instructions — Kessoku Games website

- Complete authorized website changes and run relevant validation before committing.
- Commit and push completed task changes to the configured Git remote automatically, without requesting another confirmation. The user has authorized this workflow, including deployment triggered by the website's existing hosting integration.
- Preserve unrelated local changes. Never force-push, rewrite shared history, or commit credentials, Streamlit secrets, or private NewCity operations catalogs.
- Preserve existing hosting and access settings unless the user requests a change. Report Git push and verified live deployment separately.
- Run `py -3 scripts/validate_site.py` for source changes. Check interactive changes in a browser when available and report any runtime verification limits.
