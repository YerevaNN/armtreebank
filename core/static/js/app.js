
  var core = {
    container: '#content-wrapper',
    loader: '<div class="ui _loader segment"><div class="ui active inverted dimmer"><div class="ui medium text loader">Խնդրում ենք սպասել</div></div></div>',
    init: function(){
      
      $('.ajax:not(.init)').on('click', function(event){
        
        var url = $(event.target).closest('a').attr('href');
        core.ajax.query(url);
        event.preventDefault();
        
      });
      $('.ajax:not(.init)').addClass('init');
      $('button.form-button:not(.init)').on("click", function( event ) {
        event.preventDefault(); 
      });
      $('.button.form-button:not(.init)').addClass('init');
      
    },
    semanticPlugin: {
      init: function(){
        
        $('.ui.dropdown:not(.init)').dropdown();
        $('.ui.dropdown:not(.init)').addClass('init');
        $('.ui.checkbox:not(.init)').checkbox();
        $('.ui.checkbox:not(.init)').addClass('init');
        
      },
    },
    ajax: {
      query: function( url, args ){
        if( location.pathname != url ) history.pushState({foo: 'bar'}, '', url);
		
        $(core.container).empty().html(core.loader);
        $.get(url, args, function(data){
          $(core.container).empty();
          var html = $(data), title = data.match(/<title>([\s|\S]*)<\/title>/i);
          html.find('.main-content').appendTo(core.container);
          document.title = title[1];
        });
      },
    },
    userAuth: {
      signOut: function(){
        
        var form = $("form#sign-out-form");
        
        form.ajaxForm({
          success: function( data ) {
            
            if( data.type == 'ok' )
              window.location = '/';
            else 
              alert(data.response);
            
          }
        }).submit();
        
      },
      signIn: function(){
        
        var form = $(".modal#signin-modal form");
        $('#signin-modal .message').addClass('hidden');
        
        form.ajaxForm({
          success: function( data ) {
            
            if( data.type == 'ok' )
              window.location = '/';
            else
              $('#signin-modal .message').removeClass('hidden');
            
          }
        }).submit();
        
      },
    },
    biblg: {
      author: '.bibliography-form .simple-author:first',
      text: '.bibliography-form .simple-text:first',
      selectType: function( type ) {
        
        $('.bibliography-form .query').addClass('hidden');
        var form = $('.bibliography-form .' + type + '-form');
        
        switch( type ) {
          case 'textbook':
            
            var author = $('.bibliography-form .textbook-form .textbook-author.author-field');
            if( author.find('select').length == 0 )
              $(core.biblg.author).clone().removeClass('hidden').appendTo(author);
            author.find('select[multiple=multiple]').each(function(){ $(this).attr('name', $(this).attr('name') + '[]' ); });

          break;
          case 'fiction':
          
            var form = $('.bibliography-form .fiction-form');
            if( form.find('.fiction-text input').length == 0 ) {
              var text = $(core.biblg.text).clone().removeClass('hidden');
              
              text.find('.field.text-name').addClass('hidden');
              
              if( text.find('.author-field select').length == 0 )
                $(core.biblg.author).clone().removeClass('hidden secondary').addClass('tertiary').appendTo( text.find('.author-field') );
              
              text.find('input, textarea, select').each(function(){
                $(this).attr('name', $(this).attr('name') + '0' );
              });
              
              text.appendTo(form.find('.fiction-text'));
              
            }
            
            form.find('select[multiple=multiple]').each(function(){ 
              if( $(this).attr('name').substring( $(this).attr('name')-2, $(this).attr('name') ) != '[]' )
                $(this).attr('name', $(this).attr('name') + '[]' ); 
            });
            
          break;
          case 'press':
          
            var form = $('.bibliography-form .press-form');
            if( form.find('.press-text input').length == 0 ) {
              var text = $(core.biblg.text).clone().removeClass('hidden');
              
              if( text.find('.author-field select').length == 0 )
                $(core.biblg.author).clone().removeClass('hidden secondary').addClass('tertiary').appendTo( text.find('.author-field') );
              
              text.find('input, textarea, select').each(function(){
                $(this).attr('name', $(this).attr('name') + '0' );
              });
              text.find('select[multiple=multiple]').each(function(){ $(this).attr('name', $(this).attr('name') + '[]' ); });

              text.appendTo(form.find('.press-text'));
            }
          
          break;
        }
        
        form.removeClass('hidden');
        
      },
      create: function( type ){
        
        var form = $('.bibliography-form .' + type + '-form');
        form.find('.loader').removeClass('hidden');
        form.find('.ui.button.submit').addClass('disabled');
        
        form.ajaxForm({
          success: function( data ) {
            
            if( data.type == 'ok' ) {
              alert(data.response);
              window.location.reload();
            } else
              alert(data.response);
            form.find('.loader').addClass('hidden');
            form.find('.ui.button.submit').removeClass('disabled');
            
          }
        }).submit();
        
      },
      textbook: {
        addText: function(){
          
          var form = $('.bibliography-form .textbook-form');
          
          var text = $(core.biblg.text).clone().removeClass('hidden');
          
          if( text.find('.author-field select').length == 0 )
            $(core.biblg.author).clone().removeClass('hidden secondary').addClass('tertiary').appendTo(text.find('.author-field'));
          
          var index = form.find('#texts_count').val();
          text.find('input, textarea, select').each(function(){
            $(this).attr('name', $(this).attr('name') + index );
          });
          text.find('select[multiple=multiple]').each(function(){ $(this).attr('name', $(this).attr('name') + '[]' ); });
          form.find('#texts_count').val(parseInt(index) + 1);
          text.appendTo(form.find('.textbook-texts'));
          form.find('.cancel-added-text.button').removeClass('disabled');
          
        },
        removeText: function(){
          
          var form = $('.bibliography-form .textbook-form');
          
          
          var index = form.find('#texts_count');
          index.val( index.val() - 1);
          
          if(index.val() == 0 ) form.find('.cancel-added-text.button').addClass('disabled');
          
          form.find('.textbook-texts.field .simple-text:last').remove();
          
        },
      },
      press: {
        addNumber: function(){
          
          var form = $('.bibliography-form .press-form');
          form.find('.number-checkbox').addClass('hidden');
          form.find('.number-input').removeClass('hidden');
          
        },
      },
      authorModel: {
        addDeathDate: function(event){
          
          var form = $(event.target).closest('form');
          form.find('.death-checkbox').addClass('hidden');
          form.find('.death-input').removeClass('hidden').val('');
        
        },
        create: function(event){
          
          var form = $(".modal#author-modal form");
          $('#signin-modal .message').addClass('hidden');
          
          form.ajaxForm({
            success: function( data ) {
              
              if( data.type == 'ok' ) {
                
                alert('Ավելացված է');
                $('#author-modal').modal('hide');
                $('#author-modal form').trigger('reset');
                var newOption = $(data.authors).find('option:last');
                
                $('.bibliography-form select[name*=author]').each(function(){
                  newOption.clone().prependTo(this);
                });
                
              } else $('#author-modal .message').removeClass('hidden');
              
            }
          }).submit();
          
        }
      }
    },
    toknz: {
      process: {
        submit: function(){
          var form = $('.tokenization form#tokenization-process');
          form.find('button').addClass('loading disabled');
          form.ajaxForm({
            success: function(data){
              
              if( data.type == 'ok' ) {
                $('.tokenization .result').html(data.result);
              } else
                alert(data.response);
              
              form.find('button').removeClass('loading disabled');
              
            }
          }).submit();
        },
        orientation: function(event, type) {
          $(event.target).closest('.tokens-parent').find('.tokens').addClass('hidden');
          $(event.target).closest('.tokens-parent').find('.tokens').eq(type).removeClass('hidden');
        }
      },
    },
  };
  
  setInterval(core.init, 200);
  setInterval(core.semanticPlugin.init, 200);
  
	$(window).bind("popstate", function( event ) {
		
		core.ajax.query(window.location.pathname);
		
	});
  