let form = document.getElementById("addForm")
let itemList = document.getElementById("items")
let filter = document.getElementById("filter")

/* Form submit event */
form.addEventListener("submit", addItem)
/* Delete event */
itemList.addEventListener("click", removeItem)
/* Filter event */
filter.addEventListener("keyup", filterItems)

/* Add item */
function addItem(e) {
  e.preventDefault()
  let newItem = document.getElementById("item").value
  if (newItem) {

  let li = document.createElement("li")
  li.className = "list-group-item d-flex justify-content-between"

  li.appendChild(document.createTextNode(newItem))

  let deleteBtn = document.createElement("button")
  deleteBtn.className = "btn btn-danger btn-sm float-right delete"

  deleteBtn.appendChild(document.createTextNode("X"))

  li.appendChild(deleteBtn)
  itemList.appendChild(li)
  }
}

/* Remove item */
function removeItem(e) {
  if (e.target.classList.contains("delete")) {
    if (/* confirm('Are You Sure?') */ true) {
      let li = e.target.parentElement
      itemList.removeChild(li)
    }
  }
}

/* Filter Items */
function filterItems(e) {
  let text = e.target.value.toLowerCase()
  let items = itemList.getElementsByTagName("li")

  /* convert to an array */
  Array.from(items).forEach(function (item) {
    let itemName = item.firstChild.textContent

    if (itemName.toLowerCase().indexOf(text) != -1) {
      item.style.opacity = "1"
      item.style.position = "static"
      // item.style.display = 'block'
    } else {
      item.style.opacity = "0"
      item.style.position = "absolute"
      // item.style.display = 'none'
    }
  })
}
