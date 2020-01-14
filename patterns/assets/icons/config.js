var path = require( "path" );

module.exports = {

  src: "assets/svg/icons/*.svg",
  dest: "assets/icons/",


  // CSS filenames
  datasvgcss: "ico.data.svg.css",
  datapngcss: "ico.data.png.css",
  urlpngcss: "ico.fallback.css",

  // preview HTML filename
  previewhtml: "preview.html",

  // grunticon loader code snippet filename
  loadersnippet: "grunticon.loader.js",

  // Include loader code for SVG markup embedding
  enhanceSVG: true,

  // Make markup embedding work across domains (if CSS hosted externally)
  corsEmbed: false,

  // folder name (within dest) for png output
  pngfolder: "png",

  // prefix for CSS classnames
  cssprefix: ".ico-",

  // Widths
  defaultWidth: "400px",
  defaultHeight: "400px",

  // define vars that can be used in filenames if desirable,
  // like foo.colors-primary-secondary.svg
  colors: {
  	error: "#f25111",
  	warning: "#b2a216",
  	success: "#41b38e",
	ocean: "#155366",
	ash: "#E3E3E3",
	black: "#121212",
	white: "#ffffff",
    sunrise: "#ff7264",
  },

  dynamicColorOnly: true,

  // css file path prefix
  // this defaults to "/" and will be placed before the "dest" path
  // when stylesheets are loaded. It allows root-relative referencing
  // of the CSS. If you don't want a prefix path, set to to ""
  cssbasepath: "/",

  template: path.join( __dirname, "default-css.hbs" ),
  previewTemplate: path.join( __dirname, "preview-custom.hbs" ),

  compressPNG: true
};
