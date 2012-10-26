var Desk = function(desk_id)
{
  var div = $(desk_id);
  cell_id = function(x,y)
  {
    return "desk_cell_"+x+"_"+y; 
  }
  
  this.init = function(width, height)
  {
    html = "";
    for(var x=0; x<width; x++)
      for(var y=0; y<height; y++)
      {
        cx = 50*x+1;
        cy = 50*y+1;
        html += '<div id="cell1" style="position: absolute; left: '+cx+'px; top: '+cy+'px; width: 48px; height: 48px; color:black; background-color:black;"></div>';
      }
    div.html(html);
  }
  
};
