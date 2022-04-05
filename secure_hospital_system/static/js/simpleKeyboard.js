const Keyboard = window.SimpleKeyboard.default;

const myKeyboard = new Keyboard({
  onChange: input => onChange(input),
  onKeyPress: button => onKeyPress(button)
});

function onChange(input) {
  document.querySelector("#id_password").value = input;
  console.log("Input changed", input);
}

function onKeyPress(button) {
  console.log("Button pressed", button);

  /**
   * Shift functionality
   */
   if (button === "{lock}" || button === "{shift}") handleShiftButton();
}

function handleShiftButton() {
  let currentLayout = myKeyboard.options.layoutName;
  let shiftToggle = currentLayout === "default" ? "shift" : "default";

  myKeyboard.setOptions({
    layoutName: shiftToggle
  });
}
