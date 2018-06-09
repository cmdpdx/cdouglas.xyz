let colors = ["gray", "primary", "secondary1", "secondary2"];
let current_width = 0;

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

    $('.background').append('<div class="square ' + color + '" ' + style + '></div>');
  }
}

function getDeviceSize(screenSize) {
  let deviceSize = "";

  if (screenSize < 576) {
    deviceSize = "xs";
  }
  else if (screenSize < 768) {
    deviceSize = "sm";
  }
  else if (screenSize < 992) {
    deviceSize = "md";
  }
  else if (screenSize < 1200) {
    deviceSize = "lg";
  }
  else {
    deviceSize = "xl";
  }

  return deviceSize;
}

$(window).on('resize', function() {
  let win = $(this);
  let screenSize = win.width();
  let deviceSize = getDeviceSize(screenSize);
  if (current_width != screenSize) {
    current_width = screenSize;
    $('.background').empty();
    createBackground(deviceSize);
  }
});

$(document).ready(function() {
  let screenSize = $(window).width();
  let deviceSize = getDeviceSize(screenSize);
  createBackground(deviceSize);
});
