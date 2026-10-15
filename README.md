# Robert J. Park — website

A free website and blog, hosted on GitHub Pages. GitHub builds the site automatically every time you change a file.

## Going live (about 15 minutes, best done on a laptop)

1. **Create a GitHub account** at github.com (free).
2. **Create a repository.** Tap **+ → New repository**. Name it exactly `yourusername.github.io` (using your actual GitHub username), set it to **Public**, and create it.
3. **Upload the site.** In the new repository, choose **uploading an existing file**, then drag in everything from the unzipped folder — including the `_layouts`, `_posts`, `assets` and `blog` folders. Tap **Commit changes**.
4. **Turn on Pages.** Go to **Settings → Pages**. Under *Build and deployment*, set Source to **Deploy from a branch**, branch **main**, folder **/ (root)**, and save.
5. After a minute or two the site is live at `https://yourusername.github.io`.

## Adding your domain (next week)

1. In the repository, go to **Settings → Pages → Custom domain**, enter your domain (for example `www.yourdomain.co.uk`) and save.
2. At your domain registrar, add the DNS records GitHub's Pages documentation lists for custom domains (a CNAME record for `www`, and A records for the bare domain).
3. Once GitHub shows the domain as verified, tick **Enforce HTTPS**.
4. Open `_config.yml` and set `url:` to your domain, e.g. `url: "https://www.yourdomain.co.uk"`.

If you want to move the email address to your new domain, change `email:` in `_config.yml` and the address in `contact.md`.

## Everyday editing

- **New blog post:** see `HOW-TO-POST.md`.
- **Change page text:** edit `index.html` (home), `services.md`, `about.md` or `contact.md` — tap the pencil icon on GitHub, edit, then commit.
- **LinkedIn link:** paste your profile URL into `linkedin:` in `_config.yml` and it appears in the footer.
