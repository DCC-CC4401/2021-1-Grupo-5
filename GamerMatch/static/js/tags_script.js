function Tags(element) {
  var DOMParent = element;
  var DOMList;
  var DOMInput;
  var dataAttribute;
  var arrayOfList;

  function DOMCreate() {
    let input_div = document.getElementById("input_div")
    var ul = document.createElement("ul");
    var input = document.createElement("input");
    input.style.width = '30%';
    input.style.padding = ' 6px 10px';
    input.style.margin = ' 8px 0';
    input.style.boxSizing  = ' border-box';
    input.style.borderRadius   = '4px';
    input.placeholder = 'Presione ENTER para agregar el tag escrito'
    DOMParent.appendChild(ul);
    input_div.appendChild(input); // first child is <ul>

    DOMList = DOMParent.firstElementChild; // last child is <input>

    DOMInput = input_div.lastElementChild;
  }

  function DOMRender() {
    // clear the entire <li> inside <ul>
    DOMList.innerHTML = ""; // render each <li> to <ul>

    arrayOfList.forEach(function (currentValue, index) {
      var li = document.createElement("li");
      li.innerHTML = "".concat(currentValue, " <a>&times;</a>");
      li.querySelector("a").addEventListener("click", function () {
        onDelete(index);
      });
      DOMList.appendChild(li);
    });
    setAttribute();
  }

  function onKeyUp() {
    DOMInput.addEventListener("keyup", function (event) {
      var text = this.value.trim(); // check if ',' or 'enter' key was press

      if (text.includes(",") || event.keyCode === 13) {
        // check if empty text when ',' is remove
        if (text.replace(",", "") !== "") {
          // push to array and remove ','
          arrayOfList.push(text.replace(",", ""));
        } // clear input


        this.value = "";
      }

      DOMRender();
    });
  }

  function onDelete(id) {
    arrayOfList = arrayOfList.filter(function (currentValue, index) {
      if (index === id) {
        return false;
      }

      return currentValue;
    });
    DOMRender();
  }

  function getAttribute() {
    dataAttribute = DOMParent.getAttribute("data-simple-tags");
    dataAttribute = dataAttribute.split(","); // store array of data attribute in arrayOfList

    arrayOfList = dataAttribute.map(function (currentValue) {
      return currentValue.trim();
    });
  }

  function setAttribute() {
    DOMParent.setAttribute("data-simple-tags", arrayOfList.toString());
  }

  getAttribute();
  DOMCreate();
  DOMRender();
  onKeyUp();
} // run immediately


;

(function () {
  var DOMSimpleTags = document.querySelectorAll(".simple-tags");
  DOMSimpleTags = Array.from(DOMSimpleTags);
  DOMSimpleTags.forEach(function (currentValue) {
    // create Tags
    new Tags(currentValue);
  });
})();