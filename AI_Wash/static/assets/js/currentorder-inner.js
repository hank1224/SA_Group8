var progressBar = {
    Bar : $('#progress-bar'),
    Reset : function(){
      if (this.Bar){
        this.Bar.find('li').removeClass('active'); 
      }
    },
    Next: function(){
      $('#progress-bar li:not(.active):first').addClass('active');
    },
  }
  
  progressBar.Reset();
  
  ////
  $("#Next").on('click', function(){
    progressBar.Next();
  })

