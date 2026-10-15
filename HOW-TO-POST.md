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
- To hold a post back, give it a future date. It stays hidden until that date has passed **and** you next make any change to the site (GitHub only rebuilds when something changes).
- To add an image, upload it to the `assets` folder, then put `![Description of image](/assets/your-image.jpg)` in your post.
