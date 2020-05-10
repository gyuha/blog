# Hugo Hago Theme

Hago is a simple blog theme.



## Installation

Inside the folder of your Hugo site run:

    $ cd themes
    $ git clone https://github.com/lubang/hugo-hello-programmer-theme

For more information read the official [setup guide](//gohugo.io/overview/installing/) of Hugo.


## Config

Modify your configuration:

    $ vi config.toml
    
    baseurl = "your-site-address"
    title = "your-site-name"
    
    languageCode = "ko-KR"
    DefaultContentLanguage = "kr"
    theme = "hugo-hello-programmer-theme"
    disqusShortname = "XXXX"
    googleAnalytics = "UA-XXXXXXXX-X"
    paginate = 7
    
    [author]
        name = "your-name"
        email = "your-email"
    
    [params]
        description = "desribe-your-site"

Modify images for your site:

    static/images/logo@.png (Left top logo image)
    static/images/thumbnail.png (OpenGraph tag for preview)

## Multilingual

Configure your language.

* kr (Korean, 한국어)
* en (English, a little bit stupid sentence :( Plz. Pull-request for this theme)

> You can pull request other languages or fix native sentence from exist language pack.



## Modify theme

### Pre process

```bash
npm install --global gulp-cli node-sass
npm install
```



### css make and update

```bash
$ npm install -g node-sass
```


### font-awsome

use CDN service..

* https://cdnjs.com/libraries/font-awesome



## Used javascript

* [Avoid Console Errors In Browsers That Lack A Console](https://varunpant.com/posts/avoid-console-errors-in-browsers-that-lack-a-console/)
* [Counter-Up2](https://github.com/bfintal/Counter-Up2)
* [jQuery Easing Plugin (version 1.3)](http://gsgd.co.uk/sandbox/jquery/easing/)
* [Magnific Popup](https://dimsemenov.com/plugins/magnific-popup/)
* [scrollUp 2.0.0](http://markgoodyear.com/labs/scrollup/)
* [wow.js](https://wowjs.uk/docs.html)
* [Waypoints](http://imakewebthings.com/waypoints/)
* [imagesLoaded](https://imagesloaded.desandro.com/)
* [matchHeight](https://brm.io/jquery-match-height) 

## Reference
* [Webpack: Merge Multiple Javascript Into Single File](https://code.luasoftware.com/tutorials/webpack/merge-multiple-javascript-into-single-file/)