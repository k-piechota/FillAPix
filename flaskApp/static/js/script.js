
function resume_game()
{


    for (var row = 0; row < rows; row++) {
        for (var column = 0; column < columns; column++) {
            if(filled_array[row][column] === 1){
            c.fillStyle = 'gray';
            c.fillRect(column * columnSize +1, row * rowSize+1, columnSize-2, rowSize-2);
            reprint(row, column);
            }
        }
    }
}


function fillGrid() {
   var i = 0;
    for (var row = 0; row < rows; row++) {
        for (var column = 0; column < columns; column++) {
        c.font = "12px Arial";
        c.fillStyle = "black";
        c.fillText(array[row][column], column*columnSize + columnSize/2, row*rowSize+rowSize/2);
        i++
        }
    }
    resume_game();
}


function drawBox() {
  c.beginPath();
  c.fillStyle = "white";
  c.lineWidth = 2;
  c.strokeStyle = 'black';
  for (var row = 0; row < rows; row++) {
    for (var column = 0; column < columns; column++) {
      var x = column * columnSize;
      var y = row * rowSize;
      c.rect(x, y, columnSize, rowSize);
      c.fill();
      c.stroke();
    }
  }
  c.closePath();
  fillGrid();
}


function reprint(row, column){
c.font = "12px Arial";
c.fillStyle = "black";
c.fillText(array[row][column], column*columnSize + columnSize/2, row*rowSize+rowSize/2);
}

function handleClick(e) {
  var x = Math.floor(e.offsetX / columnSize),
  y = Math.floor(e.offsetY / rowSize);
  var response = ''
  $.post('/check/' + game_id , {column: x, row: y}, function(data, status){
    if(data === 'OK' || data === 'WON'){
    c.fillStyle = 'gray';
    c.fillRect(x * columnSize +1, y * rowSize+1, columnSize-2, rowSize-2);
    reprint(y, x)
    }
    if(data === 'NOT OK')
    {
        alert('To nie jest zamalowane pole')
    }
    if(data === 'WON'){
        alert("Wygrales!");
        window.location.href = '/';
    }

  });

}

function init (board, id, filled){
canvas = document.getElementById('canvas'),
c = canvas.getContext("2d");

canvas.addEventListener('click', handleClick);
array = board;
filled_array = filled;
game_id = id,
rows = board.length,
columns = board[0].length;
rowSize = Math.floor(canvas.height/ rows),
columnSize = Math.floor(canvas.width/ columns);
drawBox();

}

function startGame()
{
    var name = document.getElementById('name').value;
    var columns = document.getElementById('columns').value;
    var rows = document.getElementById('rows').value;
    var image = document.getElementById('graphics').options[document.getElementById('graphics').selectedIndex].text;

    $.post('/start_game', {name: name, column: columns, row: rows, image: image},  function(data, status){
        if(status== 'success'){
           window.location.href = '/game/'+ data;
           }
    });



}