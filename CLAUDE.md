# Marketing agency platform (Neotech) — full handoff for Claude

Read this whole file before any work in this folder. It is self-contained: with this folder alone a new Claude (other computer, other account) can run, change, redeploy or re-brand the platform.

## 0. How to work with the user (always)
- The user is a beginner and writes Georgian. Answer in VERY short, simple Georgian: max 4 short lines / 300 characters, no plans, no jargon, numbered steps for anything they must do.
- The user often sends several messages in a row. After every user message reply ONLY „დაამთავრე?“; when they write „კი“ / „დავამთავრე“, do the work right away (no plan, never ask „დავიწყო?“).
- Change only what was asked. If something is rejected, ask in one line what exactly to change.
- Never write the long dash „—“ in any text for the user.
- Show results in the browser (built-in browser pane) and mark on screenshots when they ask „where“.
- Never type the user's own passwords. Test accounts on localhost/demo are fine. Accepting terms (e.g. Firebase) is the user's click.

## 1. What it is
A closed team web app: „ნეოტექის მარკეტინგული სააგენტო“.
- Live: https://neotechdigitalmm-sudo.github.io/neotech-posts/ (GitHub Pages, repo `neotechdigitalmm-sudo/neotech-posts`, branch `main`, root folder). This folder IS that git repo; `git push` publishes in ~1 minute.
- Backend: Firebase project `neotech-marketing` (Google account neotechdigitalmm, Spark = free). Firestore (location eur3), Authentication (Email/Password). Authorized domain added: `neotechdigitalmm-sudo.github.io`.
- No build step: plain HTML + ES modules + Firebase JS SDK 12.19.0 from gstatic.
- Demo mode: if `firebaseConfig.apiKey` in `config.js` is empty, everything runs in browser localStorage (key `neotech_plan_v3`), good for local testing.

## 2. Files
- `index.html`: all CSS (brand colours in `:root`: --blue #041E89, --navy #020C37, --orange #FF5625, grey done #7A8092) + `<script type="module" src="app.js?v=N">`.
- `app.js`: whole UI (render functions per role, modals, event binding in `bind()`).
- `store.js`: data layer with two implementations (demo / Firebase) behind one API: onAuth, hasAdmin, setupAdmin, register, login, logout, watchManagers, updateManager, deleteManager, watchProducts, addProduct, updateProduct, deleteProduct, watchSettings, saveSettings, watchNotes, addNote, updateNote. Firebase listeners use `live()` = retry on permission errors (fresh accounts).
- `config.js`: `firebaseConfig` (web config, public by design) + `BRAND` (name, title, logo, shop URL/host, login domain, brand-manager categories, post styles, default post days, confirm hours). Re-branding = edit BRAND + colours + logo.
- `firestore.rules`: security rules. After any change paste them into Firebase console → Firestore → Rules → Publish (see §7).
- `import/posts.json` + `import/posts/*.jpg` (LOCAL ONLY, in .gitignore, never on GitHub): OUR prepared posts (made by Claude/marketing): id, date, time, title, style, where, images, text, status (planned/posted), links [{network,url}], videos [Drive file id] (shown with the Drive player; the file stays on Drive, `add_post.py add --video <Drive link>`), optional productId (links to a brand upload).
- `tools/add_post.py`: add a ready post / mark posted with links / list (writes `import/`). Then: start the local server (`.claude\launch.json` → „marketing“, http://localhost:8765), marketing logs in there → „გამზადებული პოსტები“ → „📥 იმპორტი“ → „კი“: posts go into Firestore `posts` (read: approved users only, write: marketing only). The live site never serves post files.
- `fonts/` FiraGO, `raw_logo.png` (white logo; `raw_` prefix only so the parent project's image checker skips it).
- `README.md` short Georgian overview, `ინსტრუქცია_სრული.md` full Georgian guide for the user.
- Cache: browsers cache files (GitHub max-age 600). On every change bump `?v=N` everywhere (index.html → app.js, app.js → store.js/config.js/posts.json, store.js → config.js). Use a small regex replace of `\?v=OLD\b` → `?v=NEW` in all three files.

## 3. Roles and screens
Start page (no login): blue full-screen, logo, title, role buttons: ბრენდ მენეჯერი / გაყიდვების მენეჯერი / ხელმძღვანელი / მარკეტინგი. Nothing else is visible without login + approval.
- Marketing (admin, the user): created once via the setup form (first visitor of „მარკეტინგი“ when `settings/main` does not exist; the user already created it on 2026-11-18). Tabs: მთავარი, მარკეტინგი. Marketing page sections: post schedule weekday toggles; 1) brand managers' uploads (✓ pick „ვიმუშაოთ“, filters by style/brand, „▶ დაიწყე მუშაობა“ sends only picked AND confirmed products → `settings.workRequest`); 2) ready posts from posts.json with status tags ⚠ not in calendar / 📅 in calendar / ✓ published, date+time pickers (no past dates, „✕ თარიღის მოხსნა“), text edit (`settings.ourEdits`), schedule (`settings.ourSchedule`); 3) calendar (click day → edit our post text); 4) people: pending registrations (approve/reject, orange box), brand manager cards (open, edit, ↑↓ order, delete, counts incl. cancelled = mistakes), sales list, leaders list.
- Brand manager: register (brand, name, ≥1 category, username, password) → waits for approval → cabinet: 5-stage counters (sent, in work = picked, ready = our post with productId, will be posted = dated, posted = with links), „+ ახალი პროდუქტი“ (style 1/2/3 → link field shop/YouTube, up to 3 images shrunk to 1000px JPEG stored as data URLs, specs, price numeric, grey toggle „100% გადამოწმებულია“). After sending: 3 hours to edit and press grey „✓ 100% გადამოწმებულია“ (turns green, locked, cannot be undone). Not confirmed in 3h → red „⚠ 3 საათში არ დადასტურდა“ (still editable, can still confirm). After confirm only „გაუქმება“ (red „გაუქმებულია“, permanent, counted as mistake) — never delete.
- Sales manager: register → approve → tabs მთავარი + გაყიდვები. Writes notes „✎ დაწერა“ on calendar posts, ready posts without date, and brand uploads (key `prod:<id>`). Notes show to everyone as red ⚠ (calendar day flag, red box). Author can withdraw („✕ შენიშვნის გაუქმება“), marketing marks „✓ გასწორდა“. Only sales can write notes.
- Leader (ხელმძღვანელი): register → approve → only მთავარი, read-only.
- Home (მთავარი, all logged-in roles): 1) month calendar; 2) „<month> პოსტები“ table (date, photo, post, where, status, links, notes); 3) brand managers' uploads table (stage, confirmation, cancelled red).

Calendar colours (only 3 + red note flag): light green = posting weekday (future), light blue = planned, grey = published. Past months greyscale; past months show only text + links (no images). „Published“ = posts.json status posted or has links, or date already passed.

## 4. Data model (Firestore)
- `settings/main`: adminUid, postDays [0-6], ourSchedule {postKey:{date,time}}, ourEdits {postKey:text}, workRequest {at,status:'waiting'|'working'|'done',ids[]}.
- `users/{uid}`: username, role ('admin'|'brand'|'sales'|'leader'), approved (false until marketing approves; missing = treated as approved for old docs), fullName, brand, cats[], order, createdAt.
- `products/{id}`: name, link, shop, specs, price, images[dataURL], style '1'|'2'|'3', managerId, managerName, brand, status 'new', date null, createdAt, confirmed, confirmedAt, cancelled, cancelledAt, pick.
- `notes/{id}`: postKey (our post id or `prod:<productId>`), postTitle, text, authorId, authorName, createdAt, resolved, withdrawn.
- Login: username → `username@<BRAND.loginDomain>` Firebase email (not a real mailbox; password reset by email is not possible — marketing deletes and the person re-registers).

## 5. The user's decisions (keep them)
Closed site, blue minimal start page with role buttons; brand uploads go ONLY to the base (never auto into calendar); marketing + Claude decide and prepare posts; ready posts get dates from marketing; Claude then schedules them in Metricool (parent project rules) and later marks them posted with links (`tools/add_post.py posted`). Header menu like a website (text links, white underline), „ონლაინ შოპი“ links to the shop. No orange demo bar. Menu per role. Title „ნეოტექის მარკეტინგული სააგენტო“. Everything Georgian.

## 6. Daily workflow for Claude
1. Read Firestore (marketing logged in, or Firebase console) for `settings/main.workRequest`, picked products and `ourSchedule`.
2. Make posts with the parent project's skills (Neotech styles 1/2/3), save finished files in `1_social media\<product>\`.
3. `python tools/add_post.py add --id … --title … --text …/post.txt --img …/post.png --img …/cover.png --video <Drive link> --style N --where "…" [--product <productId>]`, then import on localhost:8765 (see §2). No push needed for posts.
4. Marketing sets date/time on the site → schedule in Metricool at that date → after publishing `tools/add_post.py posted --id … --link "Facebook=…" …` and import again on localhost (import keeps the date set on the site).
Not built yet: automatic pickup of „▶ დაიწყე მუშაობა“ (idea: scheduled task that reads `settings/main.workRequest` every 15 min while the computer is on, sets status 'working'/'done').

## 7. Set up for a NEW brand / new account (step by step)
1. Copy this folder. Delete `.git` if it is a new repo. Empty `posts.json` to `[]` and `posts/`.
2. Edit `config.js` → `BRAND` (name, nameGen, title, logo file, shopUrl, shopHost, loginDomain, cats, styles, postDays, confirmHours); colours in `index.html :root`; replace `raw_logo.png` (white on transparent). Favicon is an inline SVG in index.html.
3. GitHub: user signs in; create a public repo; `git init -b main`, commit, `git remote add origin https://github.com/<user>/<repo>.git`, `git push -u origin main` (Git Credential Manager opens the browser for login). Settings → Pages → Deploy from branch → main / root → Save. URL: https://<user>.github.io/<repo>/.
4. Firebase (console.firebase.google.com, the user must tick the terms): create project (Analytics off) → Authentication → Get started → Email/Password → Enable → Save → Settings → Authorized domains → add `<user>.github.io` → Firestore → Create database (Standard, location eur3, production mode) → Rules tab → paste `firestore.rules` → Publish → Project overview → Add app → Web → nickname → Register → copy `firebaseConfig` into `config.js`.
   Pasting rules into the console editor: it is CodeMirror 6. Via the browser tool: `const v=document.querySelector('.cm-content').cmView.view; v.dispatch({changes:{from:0,to:v.state.doc.length,insert:RULES}})`, then click Publish.
5. Push, open the site, choose „მარკეტინგი“ → the USER creates the admin account immediately (first one wins).
6. Test with one real person per role (register → approve → each feature). A QA checklist: §3 flows + widths 1440/1024/768/390 without horizontal scroll + no console errors.

## 8. Known limits
- Posts are in Firestore `posts` (since 2026-11-19); GitHub has no post files. Git history was rewritten on 2026-11-19 (no old post files left).
- Product images are stored inside Firestore documents (max 1 MB per doc; 3 images at 1000px JPEG fit).
- Auto-cleanup: when marketing logs in, posts dated >6 months ago, brand uploads and notes older than 6 months are deleted (`cleanupOld` in app.js). Drive videos are not touched.
- Spark free limits (Firestore 50k reads / 20k writes per day) are far above this team's use.
