var curprojid=0;
    $(".deleteTrash").on("click",function(e){
        e.preventDefault();
        $(this).parent().next().show();
        e.stopPropagation();
    });
   $(".deletecancel").on("click",function(e){
       e.preventDefault();
    $(this).parent().hide();
       e.stopPropagation();
    //alert($(this).parent().prop("class"));
});
    $(".yesdelete").on("click",function(e){
       e.preventDefault();
        //console.log($(this));
       var pid=$(this).parents("li").data("project-id");

       var data = {    'proj_id':pid,

                 }

    console.log(data)
    $.ajax({
        'url':'/home/deleteproject/',
        'method':'post',
        'data':data,
        'success': function(response){
           // alert("df");
           $(".left-panel-scroll ul").find("[data-project-id="+pid+"]").remove();
           // alert(response.projcount);
            $(".projcount").html(response.projcount+" Projects");
            $("#rightView_content").addClass("hide");
            $(".project_lists").hide();
        },
        'error':function(re){

        }
    })


e.stopPropagation();
});
var mediacurrentselection="";
var projectcurrentselection="";
$(".articles").on("click",function(){
	$(".all").removeClass("active");
	$(".videos").removeClass("active");
	$(".tracks").removeClass("active");
	$(".images").removeClass("active");
	$(".articles").addClass("active");
	$("#rightView_content").hide();
	//$(".project_lists").hide();

    mediacurrentselection="article";
    if(projectcurrentselection!=0) {
        getmediadetails(projectcurrentselection,mediacurrentselection,0);
    }
});
$(".all").on("click",function(){
	$(".all").addClass("active");
	$(".videos").removeClass("active");
	$(".tracks").removeClass("active");
	$(".images").removeClass("active");
	$(".articles").removeClass("active");
	$("#rightView_content").show();
	//$(".project_lists").show();
    //$(".project_lists .pl_thumbHolder").show();
    mediacurrentselection="";
    //alert(projectcurrentselection+" "+mediacurrentselection);
    if(projectcurrentselection!=0) {
        getmediadetails(projectcurrentselection,mediacurrentselection,0);
    }
});
$(".videos").on("click",function(){
	$(".all").removeClass("active");
	$(".videos").addClass("active");
	$(".tracks").removeClass("active");
	$(".images").removeClass("active");
	$(".articles").removeClass("active");
	$("#rightView_content").hide();
	//$(".project_lists").hide();

       mediacurrentselection="video";
    if(projectcurrentselection!=0) {
        getmediadetails(projectcurrentselection,mediacurrentselection,0);
    }
});
$(".tracks").on("click",function(){
	$(".all").removeClass("active");
	$(".videos").removeClass("active");
	$(".tracks").addClass("active");
	$(".images").removeClass("active");
	$(".articles").removeClass("active");
	$("#rightView_content").hide();
	//$(".project_lists").hide();

    mediacurrentselection="track";
    if(projectcurrentselection!=0) {
        getmediadetails(projectcurrentselection,mediacurrentselection,0);
    }
});
$(".images").on("click",function(){
	$(".all").removeClass("active");
	$(".videos").removeClass("active");
	$(".tracks").removeClass("active");
	$(".images").addClass("active");
	$(".articles").removeClass("active");
	$("#rightView_content").hide();
	//$(".project_lists").hide();

    mediacurrentselection="image";
    if(projectcurrentselection!=0) {
        getmediadetails(projectcurrentselection,mediacurrentselection,0);
    }
});
$("li").hover(function(){
    $(this).css("cursor", "pointer");
    $(this).css("cursor", "hand");
    }, function(){
});

function getmediadetails(projectid,mtype,mid)
{
      var data = {
        'project_id' :projectid,
         "mtype":mtype,
         'mid':mid,
    }
    console.log(data)
    $.ajax({
        'url':'/home/mediadetails/',
        'method':'post',
        'data':data,
        'success': function(response){
        console.log(response);
            if(mid==0) {
                display_projectlist(response.mediadata, response.mediacount);
            }
            else{
                changemodalcontent(response);
            }
        },
        'error':function(re){

        }
    });

}
    // resize
	function modalHeight() {
		videoHeight = $(window).height();
		$('.video-modal').css('height', videoHeight - 50);
	};
	modalHeight();

	$(window).resize(function() {
		modalHeight();
	});


	if ($(window).width() >= 768) {
        function setHeight() {
            windowHeight = $(window).height();
            $('#main_Content').css('min-height', windowHeight);
            $('.right_viewArea').css('min-height', windowHeight + 20);
            $('.leftPanel').css('min-height', windowHeight);
            $('.left-panel-scroll').css('height', windowHeight - 200);
        };
        setHeight();

        $(window).resize(function () {
            setHeight();
        });
        function sticky_relocate() {
			var window_top = $(window).scrollTop();
			var div_top = $('#sticky-anchor').offset().top;
			var targetOffset = $("#anchor-point").offset().top;

			if (window_top > div_top) {
				//$('.leftPanel').addClass('stick');
				$('.hd').removeClass('hide');
				$('.nav-categories').addClass('hide');
			} else {
				//$('.leftPanel').removeClass('stick');
				$('.hd').addClass('hide');
				$('.nav-categories').removeClass('hide');
			}
		}

		$(function () {
			$(window).scroll(sticky_relocate);
			sticky_relocate();
		});
    }

  //video modal
    function modalHeight() {
		videoHeight = $(window).height();
		$('.video-modal').css('height', videoHeight - 50);
	};
	modalHeight();

	$(window).resize(function() {
		modalHeight();
	});

    //$('.pl_thumbHolder .thumbnail').click(function(){
	//	$('body').css('overflow', 'hidden');
	//	$('.video-modal').fadeIn();
	//	$('.body-overlay').fadeIn();
	//})

    $( document ).on( 'click',".pl_thumbHolder .thumbnail", function(e) {

        //alert($(this).parent().data("media-id"));
        $(".video-modal").data("media-id",$(this).parent().data("media-id"));
        var m=$(this).parent().data("media-type");
        $(".video-modal").data("media-type",m);
        getmediadetails(projectcurrentselection,m,$(this).parent().data("media-id"));
        //alert($(this).parent().data("media-id")+" "+$(".video-modal").data("media-id"));
        //alert($(this).parent().data("media-type")+" "+$(".video-modal").data("media-type"));
        $('body').css('overflow', 'hidden');
		$('.video-modal').fadeIn();
		$('.body-overlay').fadeIn();
    });
var mediaurl="";
   function changemodalcontent(res){
       //console.log("-----------");
       //console.log(res[0].media_type);
       mediaurl=res[0].media_url;
       $("#mediatitle").html(res[0].media_title);
       $("#mediatitleleft").html(res[0].media_title);
       $("#uploaddate").html(" Uploaded date : "+res[0].uploaded_date.substring(0, 10));
       $("#mediadetail").html(res[0].media_details);
        if(res[0].media_type=="image")
        {
            $(".mediaplayer").replaceWith('<div class="mediaplayer"><img height="100%" src="'+res[0].media_url+'"></div>');
            $(".video-thumbnails ul li:eq(0) img").attr("src",res[0].media_url);
        }
       else if(res[0].media_type=="video"){
           $(".mediaplayer").replaceWith('<div class="mediaplayer"> <video  controls>'+
                                        '<source src="'+res[0].media_url+'" type="video/mp4">'+
                                        'Your browser does not support the video tag.'+
                                        '</video> </div>');
        }
       else if(res[0].media_type=='article'){
           $(".mediaplayer").replaceWith('<div class="mediaplayer"> <iframe width="100%" height="100%" src="'+res[0].media_url+'"></iframe></div>');
        }
       else if(res[0].media_type=='track'){
           $(".mediaplayer").replaceWith('<div class="mediaplayer"><audio controls  style="width:100%;height:30%;margin-top:25%;">'+
                                            '<source src="'+res[0].media_url+'" type="audio/ogg"></audio></div>');
        }
   }

    $('.btn-done').click(function(){
		$('body').css('overflow', 'visible');
		$('.video-modal').fadeOut();
		$('.body-overlay').fadeOut();
	})

  var myVideo=document.getElementById("videoPP"); 
  $('.play-icon, .max-icon, .prev-video, .next-video').click(function(){
    event.preventDefault();
  })
  function playPause()
  { 
    if (myVideo.paused) {
      myVideo.play(); 
      $('.play-icon').hide();
    }
    else {
      myVideo.pause(); 
      $('.play-icon').show();
    }
  } 

$('[data-toggle="popover"]').popover();

      var thumbnailset=0;
      var newprojflag="F";
var contents = $('.media-heading').html();
$('.media-heading').blur(function() {
    if (contents!=$(this).html()){
        //alert('Handler for .change() called.');
        contents = $(this).html();
        update();
    }
});
var projtype = $('.edit-projType').html();
$('.edit-projType').blur(function() {
    if (projtype!=$(this).html()){
        //alert('Handler for .change() called.');
        projtype = $(this).html();
        update();
    }
});
var projdesc = $('.edit-projDesc').html();
$('.edit-projDesc').blur(function() {
    if (projdesc!=$(this).html()){
        //alert('Handler for .change() called.');
        projdesc = $(this).html();
        update();
    }
});
var projurl = $('#mediaURL').val();
$('#mediaURL').change(function() {
    if (projurl!=$(this).val()){
        //alert('Handler for .change() called.');
        projurl = $(this).val();
        update();
    }
});

function update(){
   // alert("sd");

    //alert($("#pt").find("img").attr("src"));
    var headingcontent=$('.media-heading').html();
    var projtype=$('.edit-projType').html();
    var projdesc=$('.edit-projDesc').html();
    var projurl=$('#mediaURL').val();
    projid=0;
    if(curprojid!=0){
        console.log(curprojid)
                projid=curprojid;
                newprojflag="update";
    }
     var data = {
		'projid':projid,
        'project_title' : removebr(headingcontent.trim()),
        'project_type' : removebr(projtype.trim()),
        'project_desc' : removebr(projdesc.trim()),
        'project_url' : removebr(projurl.trim()),
        'thumbnail_url' : $("#pt").find("img").attr("src"),
        'flag' : newprojflag,
    }
    console.log(data)
    $.ajax({
        'url':'/home/projupdate/',
        'method':'post',
        'data':data,
        'success': function(response){
       // alert(response.data.id)
        $("#newprojimg").attr("data-project-id",response.data.id);
        $(".pH_row-edit").attr("data-project-id",response.data.id);
        $(".projcount").html(response.projcount+" Projects");
        //alert(response.projcount);
        $("#rightView_content").removeClass("hide");
        $("#rightView_content").find(".pH_row-edit").attr("data-project-id",response.data.id);
        $("#rightView_content").find(".media-object").attr("src",response.data.thumbnail_url);
        $("#rightView_content").find(".media-body h4").html(response.data.project_title);
        $("#rightView_content").find(".media-body .edit-projType").html(response.data.project_type);
        $("#rightView_content").find(".media-body .edit-projDesc").html(response.data.project_desc);
        $("#mediaURL").val(response.data.project_url);
      console.log(response.data.id);
      curprojid=response.data.id;
        $(".left-panel-scroll ul").find("[data-project-id="+response.data.id+"]").find("span").html(response.data.project_title);
        $(".left-panel-scroll ul").find("[data-project-id="+response.data.id+"]").find("img:eq(0)").attr("src",response.data.thumbnail_url);

     $(".projcount").removeClass("hide");
     $("#add").removeClass("hide");
     $("#cancel").addClass("hide");
        },
        'error':function(re){

        }
    })

}
 $(function() {

 $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
           });
    function getCookie(c_name)
       {
           if (document.cookie.length > 0)
           {
               c_start = document.cookie.indexOf(c_name + "=");
               if (c_start != -1)
               {
                   c_start = c_start + c_name.length + 1;
                   c_end = document.cookie.indexOf(";", c_start);
                   if (c_end == -1) c_end = document.cookie.length;
                   return unescape(document.cookie.substring(c_start,c_end));
               }
           }
           return "";
       }
   });

  $("#add").click(function(){
     curprojid=0;
     $(".projcount").addClass("hide");
     $("#add").addClass("hide");
     $("#cancel").removeClass("hide");
     $("#rightView_content").removeClass('hide');
$("#rightView_content").find(".pH_row-edit").attr("data-project-id","0");
$("#rightView_content").find(".media-object").attr("src","/static/images/Edit/titleImage.png");
$("#rightView_content").find(".media-body h4").html("Project Title");
$("#rightView_content").find(".media-body .edit-projType").html("Project Type");
$("#rightView_content").find(".media-body .edit-projDesc").html("Project Description");
$("#mediaURL").val("http://");


       newprojflag="T";
     $("#rightviewul").prepend(' <li id="newprojimg" data-project-id="0"><a>' +
             '<img src="/static/images/Edit/titleImage.png" alt="Lorem ipsum">'+
                 ' <span class="newprojtitle"></span>'+
                  '<div class="overLay"></div>'+
                  '<img src="/static/images/Edit/empty-trash.png" class="emptyTrash" alt="delete">'+
                 ' <img src="/static/images/Edit/trash.png" class="deleteTrash" alt="delete">'+
                  '</a>'+
                ' <div class="deletePrompt" style="display:none;">'+
                 ' <h4>Are you sure?</h4>'+
                 ' <a class="deletecancel">Cancel</a>'+
                 ' <a class="yesdelete">Yes, Delete</a>'+
               ' </div>'+
              '</li>');
      //alert( newprojflag);
      $(".project_lists").hide();
  });
  $("#cancel").click(function(){
     $(".projcount").removeClass("hide");
     $("#add").removeClass("hide");
     $("#cancel").addClass("hide");
     $("#rightView_content").addClass("hide");
       newprojflag="F";
     if($("#newprojimg").data("project-id")==0)
     {$("#newprojimg").remove();}
     //$("#newprojimg").addClass("hide");
     // alert( newprojflag);
  });
$("#pt").change(function (e){
    //alert("click");
    var $img= e.target.files[0];
    console.log($img);
   var projid=$("#pt").parents(".pH_row-edit").data("project-id");
   // alert(projid);
   // if(projid==0)
  //  {
    var data=new FormData();
    data.append("image",$img);
console.log(data)
$.ajax({
  url: "uploadprojthumb/",
  type: "POST",
  data: data,
  dataType: 'json',
  processData: false,  // tell jQuery not to process the data
  contentType: false,   // tell jQuery not to set contentType
  'success': function(response){
       $("#newprojimg").find("img:eq(0)").attr("src",response.proj_url);
       $("#pt").find("img").attr("src",response.proj_url);

       update();

      //alert(response.proj_url);
        },
        'error':function(re){
            alert("error in creating project");
        }
});
   // }
    });

//$("#rightviewul li").click(function(e){
$(document.body).on('click', "#rightviewul li" ,function(){

//alert("click");
    if($(this).data("project-id")!=0) {
        $(this).addClass("active");
        $(this).siblings().removeClass("active");
    }
    curprojid=$(this).data("project-id");
    projectcurrentselection=curprojid;
    //alert($(this).data("project-id"));
     var data = {
        'project_id' : $(this).data("project-id"),
         "flag":"detail",
    }
    console.log(data)
    $.ajax({
        'url':'/home/projupdate/',
        'method':'post',
        'data':data,
        'success': function(response){
        console.log(response);
$(".project_lists").show();
$("#rightView_content").removeClass("hide");
$("#rightView_content").find(".pH_row-edit").attr("data-project-id",response.projdata.id);
$("#rightView_content").find(".media-object").attr("src",response.projdata.thumbnail_url);
$("#rightView_content").find(".media-body h4").html(response.projdata.project_title);
$("#rightView_content").find(".media-body .edit-projType").html(response.projdata.project_type);
$("#rightView_content").find(".media-body .edit-projDesc").html(response.projdata.project_desc);
$("#mediaURL").val(response.projdata.project_url);

display_projectlist(response.mediadata,response.mediacount);
    $(".all").addClass("active");
	$(".videos").removeClass("active");
	$(".tracks").removeClass("active");
	$(".images").removeClass("active");
	$(".articles").removeClass("active");
	$("#rightView_content").show();

        },
        'error':function(re){

        }
    })

});

function display_projectlist(medialist,mediacount)
{
    console.log(medialist);
var e='<div class="project_lists">';
    for(i=0;i<mediacount;i++)
    {
      var mediaurl=getimgurl(medialist[i].media_type);
      e+='<div class="pl_thumbHolder"  data-media-type="'+medialist[i].media_type+'" data-media-id="'+medialist[i].id+'">'+
              '<div class="thumb-edit-overlay"></div>'+
              '<div class="thumbnail">'+
                '<img src="'+medialist[i].media_url+'" alt="demo1">'+
                '<div class="caption">'+
                  '<p>'+medialist[i].media_title+'</p>'+
                 ' <a href=""><img src="'+mediaurl+'" alt="videos"></a>'+
                '</div>'+

                '<div class="thumb-edit-icons">'+
                 ' <div class="squaredThree">'+
                  '  <input type="checkbox" value="None" id="test_1" name="check" />'+
                  '  <label for="test_1"></label>'+
                 ' </div>'+
                '</div>'+
             ' </div>'+
            '</div>';
    }
    e+="</div>";
     $(".project_lists").replaceWith(e);
}
function getimgurl(inp)
{
    if(inp=="image"){return "/static/images/header/images-black.png"}
    else if(inp=="article"){return "/static/images/header/articles-black.png"}
    else if(inp=="track"){return "/static/images/header/tracks-black.png"}
    else if(inp=="video"){return "/static/images/header/videos-black.png"}
}
function removebr(str){
    str=str.replace(/[&]nbsp[;]/gi," ");
    str=str.replace(/[<]br[^>]*[>]/gi,"");
    return str;
}


 $("#updatecoverbtn").click(function (e){
    //alert("click");

    var $img=$(this).parents("form")[0];
     console.log($img);
   // alert(projid);
   // if(projid==0)
  //  {
     e.preventDefault();
    var data=new FormData($img);
    //data.append("image",$img);
console.log(data)
$.ajax({
  url: "updatecover/",
  type: "POST",
  data: data,
  dataType: 'json',
  processData: false,  // tell jQuery not to process the data
  contentType: false,   // tell jQuery not to set contentType
  'success': function(response){

        $("#banner img").attr("src",response.coverimgurl);
        },
        'error':function(re){
           // alert("error in creating");
        }
});
   // }
    });
      $("#updateprofilebtn").click(function (e){
       var $img=$(this).parents("form")[0];
       console.log($img);
       e.preventDefault();
       var data=new FormData($img);
    //data.append("image",$img);
console.log(data)
$.ajax({
  url: "updateimg/",
  type: "POST",
  data: data,
  dataType: 'json',
  processData: false,  // tell jQuery not to process the data
  contentType: false,   // tell jQuery not to set contentType
  'success': function(response){

        $("#userProfile img:eq(0)").attr("src",response.profileimgurl);
        $(".header-profilePic img").attr("src",response.profileimgurl);
        },
        'error':function(re){
           // alert("error in creating");
        }
});
   // }
    });


//upload media
var mediatype="";
$(".icn img").on("click",function(){
    var proj=$(this).parents(".pH_row-edit").attr("data-project-id");
    mediatype=$(this).parents(".icn").data("media-type");
    //alert(mediatype);
    if(mediatype=="image"){
        $("#muploadform #media").attr("accept","image/*");
    }
    else if(mediatype=="video"){
        $("#muploadform #media").attr("accept","video/*");
    }
    else if(mediatype=="track"){
        $("#muploadform #media").attr("accept","audio/*");
    }
    else if(mediatype=="article"){
        $("#muploadform #media").attr("accept","");
    }

      });


$("#muploadform").change(function (e){
    //alert("click");
    var $file= e.target.files[0];
    var proj=$(this).parents(".pH_row-edit").attr("data-project-id");
    //var mediatype=$(".icn img").parents(".icn").data("media-type");
    console.log(mediatype+" "+proj);
    var data=new FormData();
    data.append("file",$file);
    data.append("projid",proj);
    data.append("mediatype",mediatype);
    console.log(data)
$.ajax({
  url: "handlemediaupload/",
  type: "POST",
  data: data,
  dataType: 'json',
  processData: false,  // tell jQuery not to process the data
  contentType: false,   // tell jQuery not to set contentType
  'success': function(response){
       //alert("success");
      var mediaurl=getimgurl(mediatype);
      $(".project_lists").prepend('<div class="pl_thumbHolder" data-media-type="'+mediatype+'" data-media-id="'+response.id+'">'+
              '<div class="thumb-edit-overlay"></div>'+
              '<div class="thumbnail">'+
                '<img src="'+response.media_url+'" alt="demo1">'+
                '<div class="caption">'+
                  '<p>'+response.media_title+'</p>'+
                 ' <a href=""><img src="'+mediaurl+'" alt="videos"></a>'+
                '</div>'+

                '<div class="thumb-edit-icons">'+
                 ' <div class="squaredThree">'+
                  '  <input type="checkbox" value="None" id="test_1" name="check" />'+
                  '  <label for="test_1"></label>'+
                 ' </div>'+
                 //' <a href=""><img src="/static/images/Edit/img-pen.png" alt="Edit"></a>'+
                '</div>'+
             ' </div>'+
            '</div>');

        },
        'error':function(re){
            alert("error in creating project");
        }
});
    });

$("#editmedia").on("click",function(){
    $("#mediatitleleft").attr("contentEditable","True");
    $("#mediadetail").attr("contentEditable","True");
    $(this).addClass("hide");
    $("#updatemedia").removeClass("hide");
    //alert($(".video-modal").data("media-id")+$(".video-modal").data("media-type"));
});
$("#updatemedia").on("click",function(){
    $("#mediatitleleft").attr("contentEditable","False");
    $("#mediadetail").attr("contentEditable","False");
    $(this).addClass("hide");
    $("#editmedia").removeClass("hide");

    var data = {
		'project_id':projectcurrentselection,
        'mid' :$(this).parents(".video-modal").data("media-id"),
        'media_type' : $(this).parents(".video-modal").data("media-type"),
        'media_title' : removebr($("#mediatitleleft").html().trim()),
        'media_details' : removebr($("#mediadetail").html().trim()),
        'media_url' : mediaurl,
    }
    console.log(data)
    $.ajax({
        'url':'/home/updatemedia/',
        'method':'post',
        'data':data,
        'success': function(response){
        //alert(response.id);
        },
        'error':function(re){
        alert("Error updating media");
        }
    })
});

$(document).on("click",".thumb-edit-icons .squaredThree",function(e){
//$(".thumb-edit-icons .squaredThree").on("click",function(e){
   e.preventDefault();

   e.stopPropagation();
   var ckbox=$(this).find("input[type='checkbox']");
   ckbox.prop("checked", !ckbox.prop("checked"));
   var smediaitems=$(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled");
   var len=smediaitems.length;
    //for(i=0;i<len;i++) {
    //    selectedmediaitems.push($(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled:eq("+i+")").parents(".pl_thumbHolder").data("media-id"));
    //}
    //alert(selectedmediaitems);
    //alert($(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled").parents(".pl_thumbHolder[data-media-type='video']").length);
    var selectedvideoitems=$(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled").parents(".pl_thumbHolder[data-media-type='video']").length;
    var selectedaudioitems=$(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled").parents(".pl_thumbHolder[data-media-type='track']").length;
    var selectedarticleitems=$(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled").parents(".pl_thumbHolder[data-media-type='article']").length;
    var selectedimageitems=$(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled").parents(".pl_thumbHolder[data-media-type='image']").length;
    var counttext="";
    if(selectedvideoitems!=0){counttext=selectedvideoitems+" Videos  "}
    else if(selectedarticleitems!=0){counttext+=selectedarticleitems+" Articles "}
    else if(selectedimageitems!=0){counttext+=selectedimageitems+" Images "}
    else if(selectedaudioitems!=0){counttext+=selectedaudioitems+" Tracks "}
    if(len!=0){counttext+=" are selected."}
    $(".countDisplay span").html(counttext);
    counttext="";
    $(".countDisplay").removeClass("hide");
});

//event to delete media items
var selectedmediaitems=[];
$(".countDisplay button").on("click",function(){
    var smediaitems=$(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled");
    var len=smediaitems.length;
    for(i=0;i<len;i++) {
        selectedmediaitems.push($(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled:eq("+i+")").parents(".pl_thumbHolder").data("media-id"));
    }
    alert(selectedmediaitems);

     var data = {
		'project_id':projectcurrentselection,
        'selectedmedia':selectedmediaitems,
    }
    console.log(data)
    $.ajax({
        'url':'/home/deletemedia/',
        'method':'post',
        'data':data,
        'success': function(response){
        console.log(response);
        for(i=0;i<len;i++) {
        $(".thumb-edit-icons .squaredThree input[type='checkbox']:checked:enabled:eq("+i+")").parents(".pl_thumbHolder").remove();
         }
        },
        'error':function(re){
        alert("Error updating media");
        }
    })

    selectedmediaitems=[];
});


$(window).scroll(function()
{
    if($(window).scrollTop() == $(document).height() - ($(window).height()))
    {
        alert($(document).height());
        //$.ajax({
        //url: "loadmore.php",
        //success: function(html)
        //{
        //    if(html)
        //    {
        //         $("#postswrapper").append(html);
        //        $('div#loadmoreajaxloader').hide();
        //    }else
        //    {
        //        $('div#loadmoreajaxloader').html('<center>No more posts to show.</center>');
        //    }
        //}
        //});
    }
});