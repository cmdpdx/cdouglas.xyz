let colors = ["gray", "primary", "secondary1", "secondary2"];

function createBackground(deviceSize) {
  let current = 0;
  let prev_color = "";
  let color = "";
  let limit = Math.floor($(window).height() / $(window).width() * 100) - 20;
  let num_cols =  50;
  let multiplier = 2;
  
  if (deviceSize != "xl" && deviceSize != "lg") {
    limit -= 20;
    num_cols = 25;
    multiplier = 4;
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

  $('.background').empty();
  createBackground(deviceSize);
});

$(document).ready(function() {
  let screenSize = $(window).width();
  let deviceSize = getDeviceSize(screenSize);


  console.log(screenSize);
  console.log(deviceSize);
  createBackground(deviceSize);
});