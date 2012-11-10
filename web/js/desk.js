var Desk = function(desk_id)
{
  var div = $(desk_id);
  this.hedgehogs = {};
  var hedgehog_count = 0;
  var cabbage_count = 0;
  var scenario = [];
  var execution_step=0;
  
  cell_id = function(x,y)
  {
    return "desk_cell_"+x+"_"+y; 
  }
  
  this.init = function(width, height)
  {
    var html = "";
    for(var x=0; x<width; x++)
      for(var y=0; y<height; y++)
      {
        var cx = Desk.cell_width *x;
        var cy = Desk.cell_height *y;
        html += '<div id="'+cell_id(x,y)+'" class="deskcell" style="position: absolute; left: '+cx+'px; top: '+cy+'px; width: '+Desk.cell_width +'px; height: '+Desk.cell_height +'px;"></div>';
      }
    html += '<div id="hedgehogs" style="position: absolute; left:0px; top: 0px;" ></div>';
    html += '<div id="cabbage" style="position: absolute; left:0px; top: 0px;" ></div>';
    div.html(html);
  }
  this.place = function(object_name, x, y)
  {
    $("#"+cell_id(x,y)).html('<div class="desk_'+object_name+'" style="position: absolute; left: 0px; top: 0px; width: '+Desk.cell_width +'px; height: '+Desk.cell_height +'px;""></div>');
  }
  this.hedgehog_create = function(name, x,y)
  {
    this.hedgehogs[name] = {"name": name, "x": x, "y": y, "no" : hedgehog_count};
    var html = $("#hedgehogs").html();
    var cx = Desk.cell_width  *x;
    var cy = Desk.cell_height *y;
    hedgehog_count += 1;
    html += '<div id="hh_'+this.hedgehogs[name]["no"]+'"unselectable="on" class=\"hedgehog alive\" style="position: absolute; left: '+cx+'px; top: '+cy+'px; width: '+Desk.cell_width +'px; height: '+Desk.cell_height +'px;">#'+this.hedgehogs[name]["no"]+'</div>';
    $("#hedgehogs").html(html);
  }
  this.hedgehog_move = function(name, dx,dy)
  {
    this.hedgehogs[name]["x"] += dx;
    this.hedgehogs[name]["y"] += dy;
    var no = this.hedgehogs[name]["no"];
    $("#hh_"+no).animate({
          left: '+='+Desk.cell_width*dx,
          top: '+='+Desk.cell_height*dy
    },500);
  }
  this.hedgehog_kill = function(name)
  {
    var no = this.hedgehogs[name]["no"];
    $("#hh_"+no).animate({
      opacity: 0.3
    },500);
    $("#hh_"+no).rotate({angle: 0, animateTo: 180, duration: 300});
    
    $("#hh_"+no).addClass("dead");
    $("#hh_"+no).removeClass("alive");
  }
  this.cabbage = function(from_x, from_y, to_x, to_y)
  {
    var html = $("#cabbage").html();
    var cx = Desk.cell_width  *from_x;
    var cy = Desk.cell_height *from_y;
    cabbage_count += 1;
    cid = 'cabbage_'+cabbage_count;
    html += '<div id="'+cid+'" class=\"cabbage flying\" style="position: absolute; left: '+cx+'px; top: '+cy+'px; width: '+Desk.cell_width +'px; height: '+Desk.cell_height +'px;"></div>';
    $("#cabbage").html(html);
    $("#"+cid).rotate({angle: 0, animateTo: 900, duration: 1000});
    $("#"+cid).animate({
      left: "+="+Desk.cell_width * (to_x - from_x),
      top: "+="+Desk.cell_height * (to_y - from_y)
    },1000, function(){
      $("#cabbage").remove();
    });
  }
  this.scenario = function(scen, step)
  {
    scenario = scen;
    execution_step = 0;
    Desk.instance = this;
    setInterval(this.step, 1000);
  }
  this.step = function()
  {
    var script = scenario[execution_step];
    for(i in script)
    {
      action = script[i];
      if(action["place"] != undefined)
        Desk.instance.place(action["place"],action["x"], action["y"]);
      else if(action["create"] != undefined)
        Desk.instance.hedgehog_create(action["create"],action["x"], action["y"]);
      else if(action["move"] != undefined)
        Desk.instance.hedgehog_move(action["move"],action["x"], action["y"]);
      else if(action["throw"] != undefined)
        Desk.instance.cabbage(Desk.instance.hedgehogs[action["throw"]]["x"],Desk.instance.hedgehogs[action["throw"]]["y"],action["x"],action["y"]);
      else if(action["kill"] != undefined)
      {
        Desk.instance.hedgehog_kill(action["kill"]);
      }
      else
        alert("Unknonw action");
    }
    execution_step += 1;
    //setTimeout(this.step(), 1000);
  }
  
};

Desk.cell_width = 32
Desk.cell_height = 32