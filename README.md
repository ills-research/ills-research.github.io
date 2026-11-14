# ILLS website template

Open `site/index.html` in a browser for the English homepage; use **FR** for French. The site is complete static HTML with local images, CSS and local JavaScript for navigation and publication search. Reading it does not require a server, an account, a package manager, or a purchased domain.

## Make a change

Edit the source below, restore static assets in a fresh checkout with `unzip -qo ills-site-assets.zip -d .`, then run `python3 -B build.py` from this folder and open the result in `site/`. Both languages are generated together. Avoid editing generated HTML directly: the next build replaces it.

| To update | Edit |
| --- | --- |
| Homepage, navigation, footer, page descriptions | `build.py` |
| Research titles, questions and examples | `content/research.py` (`AXES` and `FR_AXES` share the same stable section IDs) |
| Research page layout and section links | `content/programme.py` |
| Funding, research chairs and industry partners | `content/funding.py` holds bilingual entries, public sources and member profile slugs. Each entry appears while at least one linked researcher is in the directory’s Members category. Funding agencies and industry partners display linked logos. Their member slugs determine eligibility. |
| Laboratory, leadership and contact | `content/laboratory.py` |
| Directory names, membership, affiliations, biographies, professional links and portrait sources | `content/members.json` |
| Doctoral projects, universities, co-advisors, professional links and portrait sources | `content/students.json` groups projects by cotutelle or co-advising. Store student portraits in `site/assets/students/`. A card displays initials when its image is omitted. |
| Visiting researchers and their professional webpages, in surname order | `content/visitors.json` |
| People / Équipe layout | `content/people.py` and `site/assets/people.css` |
| Publication catalogue | `content/publication_periods.json` defines the eligible members and years. Run `python3 -B tools/publication_review/refresh.py` with internet access to refresh the reviewed records in `content/publication_catalogue.json`, then rebuild. New proceedings outside the approved venue list appear in the local review for a decision. |
| Joint research publications | The monthly catalogue refresh also checks paper-level France–Canada coauthorship in HAL and OpenAlex. The lab’s reviewed DBLP keys from its activity-report bibliography are in `content/joint_references.json`. The bilingual section combines matching preprints and published versions; the main catalogue retains each record. |
| Partner institutions and exchanges on the homepage | `content/network.py` |
| Seminar programme | `content/seminars.json` holds dates, Montréal times, speakers, original titles, abstracts and short bilingual biographies. Use a labelled research overview when only a title is announced. The Events page groups seminars by date. |
| Workshops and research openings | `content/listings.py` (add dated meetings to `CALENDAR` and recruitment notices to `OPENINGS`) |
| CNRS application resources and laboratory news | `content/listings.py` (edit `render_applications` for application links and `NEWS` for dated stories in both languages) |
| Colour, typography and responsive layouts | `site/assets/style.css` and the page stylesheets next to it |
| Navigation behaviour | `site/assets/site.js` |
| Photographs and logos | `site/assets/` |

Keep the original scientific-project PDF outside the website repository and release archives. Update the public research summaries in `content/research.py`.

The seven navigation pages are Overview, People, Research, Events, Openings, CNRS mobility and News. Overview includes the laboratory, partners and contact details. Research includes the full publication catalogue under `#publications`. The homepage and footers link to it, and directory entries and profiles link to the corresponding member filter. The old page addresses redirect in both languages. Keep the redirect files when deploying.

Give each calendar entry a stable ID, bilingual event type, and ISO start date. Add an end date for a multi-day meeting. Events stay in Upcoming through their final day in Montréal, then move to the archive.

To preview over HTTP: `python3 -m http.server 8000 --bind 127.0.0.1 --directory site`, then open `http://127.0.0.1:8000/`. Run `python3 -B tools/check_site.py` after changes to check all local references, section targets and language pairs.

## Publish and maintain

See [LAUNCH.md](LAUNCH.md) to publish from the ILLS GitHub organization and connect the domain after purchase. Only `site/` is deployed. GitHub Actions restores `ills-site-assets.zip`, generates both language editions, checks local links, and publishes the result. For offline copies, check in both the source and the generated HTML. URLs are relative, so the same files work at a domain root or in a repository subdirectory.

## Asset and content notes

- The site uses the supplied colour logo on white and the navy-background variant on dark sections.
- The 2024 team portrait comes from the photograph `ILLS_2.jpg` supplied by ILLS. Its web versions are in `site/assets/photos/`.
- Individual portraits are stored in `site/assets/people/`. Each entry in `content/members.json` records the professional profile, original portrait URL and source. Keep entries in surname order. Set a member’s `status` to `current`, `associate`, `past`, `visiting` or `student` to place them in the corresponding section in both languages. For example, `associate` lists a person under **Associate members** in English and **Membres associés** in French. The two leadership entries also specify a display order.
- Each current and associate member has a `biography` entry that generates an English and a French page. Keep the slug stable, write one short research paragraph in each language, and pair the translations of each topic. The page uses the directory affiliation unless you specify bilingual `appointments`. Use `website` and `website_label` for an academic page or group site; add `scholar` and `linkedin` only when you have verified the account. Cards without biographies still open their original external profile.
- The two photographs of the laboratory premises come from the supplied scientific project (Pavillon F: section 8.1, figure 2a; ILLS entrance: appendix B, figure 3). Partner marks were extracted from the report and the lab’s institutional logo library.
- The homepage surface is an original mathematical illustration of a sampled tube around a trefoil curve. The four smaller illustrations are also generated, and do not represent experimental results. Optional artwork source is in `tools/artwork.py` (requires NumPy and Pillow); normal site builds do not need these packages.
- The structure draws on [BAIR](https://bair.berkeley.edu/) for the lab overview and [ELLIS](https://ellis.eu/research/programs) for connecting programme descriptions and participating institutions. The design and scientific content are specific to ILLS.
- Current institutional information is supported by the [CNRS lab profile](https://ottawa.office.cnrs.fr/en/research/international-laboratory-on-learning-systems-2/), the [ÉTS founding announcement](https://www.etsmtl.ca/en/news/international-lab-dedicated-to-ai-kicks-off-in-montreal) and the [director’s site](https://pablo-piantanida.org/). Publication records provide BibTeX and available arXiv and publisher links.
