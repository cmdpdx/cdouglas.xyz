let colors = ["gray", "primary", "secondary1", "secondary2"];

let win = {
  currentScreenSize: 0,
  deviceSize: '',
  numCols: 0,
  rowLimit: 0,
  multiplier: 1
};

let $root = $('html, body');


function createBackground() {
  let current = 0;
  let prev_color = "";
  let color = "";
  
  for (let i = 0; i < 150; i++) {
    current += 1 + (Math.floor(Math.random() * 2));
    if (Math.floor(Math.random() * 3) < 1) {
      current += i;
    }
    let x = (current % win.numCols) * win.multiplier;
    let y = Math.floor(current / win.numCols) * win.multiplier;

    if (y > win.rowLimit) {
      break;
    }

    let style = 'style="left: ' + x + 'vw; top: ' + y + 'vw; width: ' + win.multiplier + 'vw; height: ' + win.multiplier + 'vw;"';

    // don't repeat colors in adjacent squares
    while (color === prev_color) {
      color = colors[Math.floor(Math.random() * 4)];
    }
    prev_color = color;

    $('.title-background').append('<div class="square ' + color + '" ' + style + '></div>');
  }
}

function footerSquares() {
  let prev_color = '';
  let color = '';
  
  for (let i = 0; i < win.numCols; i++) {
    let x = i * win.multiplier;
    let style = 'style="left: ' + x + 'vw; bottom: 0vw; width: ' + win.multiplier + 'vw; height: ' + win.multiplier + 'vw;"';
    // don't repeat colors in adjacent squares
    while (color === prev_color) {
      color = colors[Math.floor(Math.random() * 4)];
    }
    prev_color = color;
    
    $('#projects').append('<div class="square ' + color + '" ' + style + '></div>');
  }
}

function comingSoon(parent) {
  let colors = ["gray", "primary", "secondary1", "secondary2"];

  for (let i = 0; i < 4; i++) {
    let color = colors.splice(Math.floor(Math.random() * colors.length), 1);
    let left = (i%2) * 50;
    let top = Math.floor(i/2) * 50;
    let style = 'style="position: absolute; width: 50%; height: 50%; left: ' + left + '%; top: ' + top + '%; z-index: 1;"'; 
    $(parent).append('<div class="' + color + '" ' + style + '></div>');
  }

  $(parent).append('<div class="coming-soon-title" style="position: relative; top: 25%; margin: auto; z-index: 2;">Coming Soon!</div>')
}


function getDeviceSize(screenSize) {
  if (screenSize < 576) {
    return "xs";
  }
  else if (screenSize < 768) {
    return "sm";
  }
  else if (screenSize < 992) {
    return "md";
  }
  else if (screenSize < 1200) {
    return "lg";
  }
  else {
    return "xl";
  }
}

$(window).on('resize', function() {
  let newScreenSize = $(this).width();
  let newDeviceSize = getDeviceSize(newScreenSize);
  if (win.currentScreenSize != newScreenSize) {
    oldDeviceSize = win.deviceSize;
    setWin();
    $('.title-background').empty();
    createBackground();
    
    if (oldDeviceSize != newDeviceSize) {
      //redraw the bottom squares
      //footerSquares();
    }
  }

});

function setWin() {
  win.screenSize = $(window).width();
  win.deviceSize = getDeviceSize(win.screenSize);
  
  // Default case: screen size of lg or xl
  win.rowLimit = Math.floor($(window).height() / $(window).width() * 100) - 20;
  win.numCols =  50;
  win.multiplier = 2;
  
  // For smaller screens, decrease columns and increase multiplier as necessary
  switch (win.deviceSize) {
    case "md":
      win.rowLimit -= 15;
      win.numCols = 33;
      win.multiplier = 3;
      break;
    case "sm":
      win.rowLimit -= 20;
      win.numCols = 25;
      win.multiplier = 4;
      break;
    case "xs":
      win.rowLimit -= 20;
      win.numCols = 20;
      win.multiplier = 5;
      break;
    default:
      break;
  }
  
}
$(document).ready(function() {
  setWin();
  createBackground();
  //footerSquares();
  $('.coming-soon').each(function (index, item) {
    comingSoon(item);
  });

  // Select all links with hashes
  $('a[href*="#"]')
    // Remove links that don't actually link to anything
    //.not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
      // On-page links
      if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
        && 
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        // Does a scroll target exist?
        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          $('html, body').animate({
            scrollTop: target.offset().top-75
          }, 700, function() {
            // Callback after animation
            // Must change focus!
            var $target = $(target);
            $target.focus();
            if ($target.is(":focus")) { // Checking if the target was focused
              return false;
            } else {
              $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
              $target.focus(); // Set focus again
            };
          });
        }
      }
    });
});
