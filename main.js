let colors = ["gray", "primary", "secondary1", "secondary2"];
let currentScreenSize = 0;

function createBackground(deviceSize) {
  let current = 0;
  let prev_color = "";
  let color = "";
  
  // Default case: screen size of lg or xl
  let limit = Math.floor($(window).height() / $(window).width() * 100) - 20;
  let num_cols =  50;
  let multiplier = 2;
  
  // For smaller screens, decrease columns and increase multiplier as necessary
  switch (deviceSize) {
    case "md":
      limit -= 15;
      num_cols = 33;
      multiplier = 3;
      break;
    case "sm":
      limit -= 20;
      num_cols = 25;
      multiplier = 4;
      break;
    case "xs":
      limit -= 20;
      num_cols = 20;
      multiplier = 5;
      break;
    default:
      break;
  }
  
  for (let i = 0; i < 150; i++) {
    current += 1 + (Math.floor(Math.random() * 2));
    if (Math.floor(Math.random() * 3) < 1) {
      current += i;
    }
    let x = (current % num_cols) * multiplier;
    let y = Math.floor(current / num_cols) * multiplier;

    if (y > limit) {
      break;
    }

    let style = 'style="left: ' + x + 'vw; top: ' + y + 'vw; width: ' + multiplier + 'vw; height: ' + multiplier + 'vw;"';

    // don't repeat colors in adjacent squares
    while (color === prev_color) {
      color = colors[Math.floor(Math.random() * 4)];
    }
    prev_color = color;

    $('.title-background').append('<div class="square ' + color + '" ' + style + '></div>');
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
  let screenSize = $(this).width();
  let deviceSize = getDeviceSize(screenSize);
  if (currentScreenSize != screenSize) {
    currentScreenSize = screenSize;
    $('.title-background').empty();
    createBackground(deviceSize);
  }
});

$(document).ready(function() {
  let screenSize = $(window).width();
  let deviceSize = getDeviceSize(screenSize);
  createBackground(deviceSize);
  $('.coming-soon').each(function (index, item) {
    comingSoon(item);
  });

});
