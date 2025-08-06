# Patterns - CSS, etc for IATI Standard repository

## History 

There was a full build system here, however unfortunately that build system was abandoned and very old. 
The build process was completely broken - it was a node project that wanted Python 2 installed!

Also, we don't want a special build system for this website as ideally in the future we want to 
move to the new IATI design system: https://github.com/IATI/design-system/
So we want to be using whatever build system that is using.

## Current Situation

patterns/converted-html/assets/css/screen.css is the CSS that is collected by the Python compressor 
tool and used in our Django Wagtail app.

## How to edit the CSS

Edit patterns/converted-html/assets/css/screen.css directly.

You may find it useful to refer back the state of the Git repository at commit 
9c3347bf34accb88ad916869fd7eb550abb270de and look at the original SCSS. It has variables, mixins and 
comments which may help you understand where the current CSS came from, and work out what changes you 
should make.

Native CSS variables are now considered safe to use; feel free to make new ones or put old ones back 
if it helps you.
https://caniuse.com/css-variables

When the CSS is changed, the compress command must be run. Restarting the web container will also trigger this automatically.

## Lint

CSS is linted with prettier, please run this before checking in.

In `patterns` directory:

```
npm install
npx prettier converted-html/assets/css/ --write
```

