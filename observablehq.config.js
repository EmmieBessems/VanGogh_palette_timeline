// See https://observablehq.com/framework/config for documentation.
let today = new Date();

export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Observable Tool",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  // pages: [
  //   {
  //     name: "Examples",
  //     pages: [
  //       {name: "Dashboard", path: "/example-dashboard"},
  //       {name: "Report", path: "/example-report"}
  //     ]
  //   }
  // ],

  // Content to add to the head of the page, e.g. for a favicon:
  head: '<link rel="icon" href="observable.png" type="image/png" sizes="32x32">',

  // The path to the source root.
  root: "src",

  // Some additional configuration options and their defaults:
  theme: "default", // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  footer: `Painting and period data taken from <a href="https://data.spinque.com/ld/data/vangoghworldwide/">Van Gogh Worldwide</a> <br>
          Letter data taken from <a href="https://data.spinque.com/ld/data/vangoghworldwide/van_gogh_letters/">Vincent Van Gogh - The Letters (Jansen, Luijten, and Bakker, 2009)</a> <br>
          Painting images taken from <a href="https://data.mendeley.com/datasets/3sjjtjfhx7/2">Van Gogh Paintings dataset (Kim, 2022)</a> <br>
          Last built ${today}`,
  // footer: "Painting and period data taken from vangoghworldwide.org, painting images taken from 'Van Gogh Paintings dataset' - Kim, A. 2022 (DOI: 10.17632/3sjjtjfhx7.2), letter data taken from vangoghletters.org", // what to show in the footer (HTML)
  sidebar: true, // whether to show the sidebar
  toc: false, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // cleanUrls: true, // drop .html from URLs
};
