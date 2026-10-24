# How to add a blog post

You can do this from your phone in the GitHub app or in a web browser.

1. Open your website's repository on github.com and go into the `_posts` folder.
2. Tap **Add file → Create new file**.
3. Name the file with the date and a short title, joined by hyphens, ending in `.md`:

   `2026-11-02-what-cbam-means-for-ni-manufacturers.md`

4. Paste this at the very top, then write your post underneath:

   ```
   ---
   title: "What CBAM means for NI manufacturers"
   tags: [Carbon, CBAM]
   ---

   Your first paragraph goes here.

   ## A subheading

   More text. **Bold** and *italic* work. So do [links](https://example.com).

   - Bullet points
   - like this
   ```

5. Tap **Commit changes**. The post appears on the site within a couple of minutes.

## Tips

- The first paragraph is used as the summary on the blog list and home page, so make it count.
- To edit or delete a post later, open its file in `_posts` and use the pencil (edit) or bin icon.
- To schedule a post, give it a future date and time, e.g. `date: 2026-11-02 12:00:00 +0000`. The site rebuilds itself every day shortly after noon (the *Publish scheduled posts* workflow in `.github/workflows`), so a post dated for noon appears then. For any other time, open the **Actions** tab, choose *Publish scheduled posts* and press **Run workflow** once the time has passed.
- To add a consultation response, copy `_posts/2026-10-24-response-historic-environment-policy.md`: keep `categories: [consultation-responses]` and fill in `consulting_body`, `closed`, `outcome` and `pdf`. Put the PDF in `assets/consultations/`. It then appears on the Consultation responses page and in the blog.
- To add an image, upload it to the `assets` folder, then put `![Description of image](/assets/your-image.jpg)` in your post.
