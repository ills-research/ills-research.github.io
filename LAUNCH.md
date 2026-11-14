# Publish the ILLS website

The lab’s GitHub organization, **ills-research**, is ready. When the site is ready to launch, use the steps below to publish it at its free `github.io` address. You can connect the purchased domain later. [Open the ILLS organization](https://github.com/ills-research)

## 1. Create the website repository

Sign in with an account that can create repositories in **ills-research**. With the organization selected as owner, create an empty **public** repository named `ills-research.github.io`. Leave the initialization options unchecked. After deployment, the site will be available at `https://ills-research.github.io/`. A public repository supports Pages on GitHub Free. [GitHub Pages site types](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## 2. Publish the template

In the repository, open **Settings → Pages → Build and deployment** and select **GitHub Actions** as the source. The template already includes the publishing workflow. [GitHub’s publishing source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

From the clean template directory containing `site/` and `.github/`, run the following commands for the first upload. Review the staged file list before committing, since the repository and its files will be public.

```sh
git init -b main
git add .
git status --short
git commit -m "Add the ILLS website"
git remote add origin https://github.com/ills-research/ills-research.github.io.git
git push -u origin main
```

Open **Actions → Publish ILLS website** and follow the deployment link when the run finishes. The workflow uploads the contents of `site/`. Open the homepage, navigate to a research axis, and switch languages to verify both editions. If the first push occurred before Pages was enabled, select **Run workflow** on the `main` branch to deploy it.

For later updates, edit the content files listed in the README. Every push to `main` that changes these sources or website assets rebuilds the English and French pages, checks their internal links, and republishes `site/`.

## 3. Connect the domain after purchase

1. In **organization Settings → Pages → Add a domain**, enter the purchased base domain. Add GitHub’s TXT verification record at the DNS provider, click **Verify** in GitHub, and retain the TXT record. [Verify a domain for an organization](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
2. In **repository Settings → Pages → Custom domain**, enter the preferred address, such as `www.example.org`, and click **Save** before changing website DNS records. This workflow stores the custom domain in repository settings.
3. At the DNS provider, point the `www` host to `ills-research.github.io` with a **CNAME** record. For the base domain, use an **ALIAS** or **ANAME** to `ills-research.github.io` if supported, or use GitHub’s published **A** records. Configure both addresses so GitHub can redirect to the preferred one. [GitHub’s DNS values and examples](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
4. When GitHub finishes its DNS check and provisions the certificate, select **Enforce HTTPS** in repository Pages settings. Visit the base domain and the `www` address to confirm both reach the lab site over HTTPS. [GitHub’s HTTPS guide](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
