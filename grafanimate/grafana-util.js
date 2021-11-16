// http://stackoverflow.com/questions/5538972/console-log-apply-not-working-in-ie9/5539378#5539378
if (Function.prototype.bind) {
  window.log = Function.prototype.bind.call(console.log, console);
} else {
  window.log = function () {};
}

// https://gist.github.com/chrisjhoughton/7890303
var waitForElement = function (selector, callback) {
  if (jQuery(selector).length) {
    callback();
  } else {
    setTimeout(function () {
      waitForElement(selector, callback);
    }, 100);
  }
};

// https://stackoverflow.com/a/33507307
$.fn.findByContentText = function (text) {
  return $(this)
    .contents()
    .filter(function () {
      return $(this).text().trim() == text.trim();
    });
};
