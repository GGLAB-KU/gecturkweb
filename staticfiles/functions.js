var showEle = document.getElementById("show-id");
function myFunction() {
    let textarea = document.getElementById("inputText");
    textarea.select();
    document.execCommand("copy");
}
function visibleFunction() {
    showEle.style.display = "block";
}

function copyDivToClipboard() {
        var range = document.createRange();
        range.selectNode(document.getElementById("copy"));
        window.getSelection().removeAllRanges(); // clear current selection
        window.getSelection().addRange(range); // to select text
        document.execCommand("copy");
        window.getSelection().removeAllRanges();// to deselect
  }

document.querySelector('.button').onmousemove = function (e) {
  var rect = e.target.getBoundingClientRect();
  var x = e.clientX - rect.left;
  var y = e.clientY - rect.top;

  e.target.style.setProperty('--x', x + 'px');
  e.target.style.setProperty('--y', y + 'px');
};

