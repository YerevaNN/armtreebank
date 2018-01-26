
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
      },
      sentence: function(biblg, sentence, pos){
        $.post('/tokenization/tokens/' + biblg + '/sentence/' + sentence + '/', {}, function(data){
          if(data['type'] == 'ok') {
            var html = $(data['res']);
            var width = 100 / html.find('.token_item').length;
            html.find('.tokens').css( 'width', ( html.find('.token_item').length * 100 ) + '%');
            html.find('.tokens').data('width', width).data('pos', 0).data('len', html.find('.token_item').length);
            if( pos ) html.find('.tokens').css('margin-left', pos['margin']).data('pos', pos['pos']);
            html.find('.token_item').outerWidth( width + '%');
            $('.tokenization .result').html(html);

            $('.modal#check-tokenization .content .tok-res').val(data['tokenization']);
            $('.modal#check-tokenization .content .sentence').val(data['sentence']);
            $('.modal#check-tokenization .content .biblg').val(data['biblg']);

            $('.modal#dep-tree .content .dep-tree').val(data['dep_tree'].replace(/\\t/g, '\t'));
            $('.modal#dep-tree .content .dep-tree-formui').empty();
            updateDepTreeForm();

            $('.modal#dep-tree .content .sentence').val(data['sentence']);
            $('.modal#dep-tree .content .biblg').val(data['biblg']);
          }
        });
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
      biblg: function(event){
        var a = $(event.target).closest('a');
        a.addClass('loading');
        
        $.post(a.attr('href'), function(data){
          
          a.removeClass('loading');
          if( data.type == 'ok' ) window.location = '/tokenization/tokens/' + data.id + '/'
          else alert(data.response);
          
        });
        event.preventDefault();
      }
    },
    tag: {
      biblg: function(event){
        var a = $(event.target).closest('a');
        a.addClass('loading');
        
        $.post(a.attr('href'), function(data){
          
          a.removeClass('loading');
          if( data.type == 'ok' ) window.location = '/tokenization/tokens/' + data.id + '/'
          else alert(data.response);
          
        });
        event.preventDefault();
      }
    },
    t_ui: {
      prevSentence: function(){
        var sentence = $('.tokenization .result .sentence').data('sentence'),
            biblgID = $('.tokenization').data('biblg');
        
        if(!sentence) sentence = 2;
        
        $('.tokenization .sentence').html('<div class="ui message">Խնդրում ենք սպասել..</div>');
        core.biblg.sentence(biblgID, sentence - 1);
      },
      nextSentence: function(){
        var sentence = $('.tokenization .result .sentence').data('sentence'),
            biblgID = $('.tokenization').data('biblg');
        
        if(!sentence) sentence = 0;
        
        $('.tokenization .sentence').html('<div class="ui message">Խնդրում ենք սպասել..</div>');
        core.biblg.sentence(biblgID, sentence + 1);
      },
      submitWord: function(event, pos){
        var token = $(event.target).closest('.token_item').data('token'),
            sentence = $(event.target).closest('.sentence').data('sentence'),
            biblg = $(event.target).closest('.sentence').data('biblg');
        
        $(event.target).addClass('loading');
        
        $.post('/tokenization/token/submit/' + pos + '/', {'token': token, 'sentence': sentence, 'biblg': biblg}, function(data){
          $(event.target).removeClass('loading');
          if(data['type'] == 'ok') {
            if( data['act'] == 'drop' ) $(event.target).removeClass('green');
            else {
              $(event.target).closest('.token_item').find('.ui.button').removeClass('green');
              $(event.target).addClass('green');
            }
            if( data['tree_tagged'] )
              tagCurrSentence();
          }
          else $(event.target).addClass('red');
        });
      },
      checkWord: function(){
        $('.ui.modal#check-word').modal('show');
      },
      newWord: function(id){
        $('.modal#new-word .button').removeClass('red').removeClass('green');
        $('.modal#new-word .form').trigger('reset');

        var word = $('.sentence .tokens .token_item#t-' + id).data('word');
        try {
          word = word.toLowerCase();
        } catch(e){}
        
        $('.ui.modal#new-word input[name=word]').val(word);
        $('.ui.modal#new-word').modal('show');
      },
      prevWord: function(){
        if( $('.tokens').data('pos') == 0 ) var pos = -( $('.tokens').data('len') - 1 ) * 100 ;
        else var pos = $('.tokens').data('pos') + 100;
        $('.tokens').css('margin-left', pos + '%').data('pos', pos);
      },
      nextWord: function(){
        if( $('.tokens').data('pos') == -( $('.tokens').data('len') - 1 ) * 100 ) var pos = 0 ;
        else var pos = $('.tokens').data('pos') - 100;
        $('.tokens').css('margin-left', pos + '%').data('pos', pos);
      },
      openFields: function(pos){
        $('.modal#new-word .extra.field').removeClass('hidden');
        $('.modal#new-word .extra.field .pos').addClass('hidden');
        $('.modal#new-word .extra.field .pos.' + pos).removeClass('hidden');
        $('.modal#new-word').modal('refresh');
      },
      nounTplFields: function(type){
        $('.modal#new-word .extra.field .pos.noun .features').addClass('hidden');
        $('.modal#new-word .extra.field .pos.noun .features.' + type).removeClass('hidden');
        $('.modal#new-word').modal('refresh');
      },
      verbTplFields: function(type){
        $('.modal#new-word .extra.field .pos.verb .features').addClass('hidden');
        $('.modal#new-word .extra.field .pos.verb .features.' + type).removeClass('hidden');
        $('.modal#new-word').modal('refresh');
      },
      wordOverview: function(){
         var form = $('.modal#new-word .form');
    
        form.ajaxSubmit({
          url: '/tokenization/word/overview/',
          success: function( data ) {
            if( data['type'] == 'ok' ) {
              $('.modal#new-word .overview').html( data['output'] );
            }
          }
        });
      },
      checkTokenization: function(){
        $('.modal#check-tokenization').modal('show');
      },
      saveTokenization: function(){

        var form = $('.modal#check-tokenization .form');
        form.find('.button').addClass('loading');

        form.ajaxForm({
          success: function( data ) {
            form.find('.button').removeClass('loading');
            if( data['type'] == 'ok' ) {
              form.find('.button').addClass('green');
              tagCurrSentence();
              setTimeout(function(){ 
                $('.modal#check-tokenization').modal('hide');
                form.find('.button').removeClass('green');
              }, 500);
            } else form.find('.button').addClass('red');
          }
        }).submit();

      },
      viewTree: function(){
        $('.modal#dep-tree').modal('show');
      },
      saveTree: function(){

        var form = $('.modal#dep-tree .form');
        form.find('.button').addClass('loading');

        form.ajaxForm({
          success: function( data ) {
            form.find('.button').removeClass('loading');
            if( data['type'] == 'ok' ) {
              form.find('.button').addClass('green');
              setTimeout(function(){ 
                $('.modal#dep-tree').modal('hide');
                form.find('.button').removeClass('green');
              }, 500);
            } else form.find('.button').addClass('red');
          }
        }).submit();


      },
    },
  };
  
  function saveNewWord() {
    $('.modal#new-word .button').addClass('loading');

    var form = $('.modal#new-word .form');
    
    var disableFields = form.find('.field.extra .hidden.pos');
    var copyFields = disableFields.clone();
    copyFields.find('.init').each(function(){
      $(this).removeClass('init');
    });

    disableFields.remove();

    form.ajaxForm({
      success: function( data ) {
        $('.modal#new-word .button').removeClass('loading');
        if( data['type'] == 'ok' ) {
          $('.modal#new-word .button').addClass('green');
          tagCurrSentence();
          setTimeout(function(){ $('.modal#new-word').modal('hide') }, 500);
        } else $('.modal#new-word .button').addClass('red');

        copyFields.appendTo(form.find('.field.extra'));
      }
    }).submit();
  }
  
  function tagCurrSentence(){
    var sentence = $('.tokenization .result .sentence').data('sentence'),
        biblgID = $('.tokenization').data('biblg');
    
    var pos = {
      'margin': $('.tokenization .tokens-block .tokens').css('margin-left'),
      'pos': $('.tokenization .tokens-block .tokens').data('pos')
    };
    $('.tokenization .tokens-block').html('Loading..');
    core.biblg.sentence(biblgID, sentence, pos);
  }

  var depLabels = ['nsubj', 'list', 'obj', 'iobj', 'csubj', 'ccomp', 'xcomp', 'obl', 'vocative', 'expl', 'dislocated', 'advcl', 'advmod', 'discourse', 'aux', 'cop', 'mark', 'nmod', 'appos', 'nummod', 'acl', 'amod', 'det', 'clf', 'case', 'conj', 'cc', 'fixed', 'flat', 'compound', 'parataxis', 'orphan', 'goeswith', 'reparandum', 'punct', 'root', 'dep'];
  var deprelOptions = '';
  depLabels.forEach(function(i){ deprelOptions += '<option value="'+i+'">'+i+'</option>'});
  var depRelSelect = '<select><option disabled selected>Deprel</option>' + deprelOptions + '</select>';

  function updateDepTreeForm(){
    var tree = $('.modal#dep-tree .dep-tree').val();
    var treeUI = $('.modal#dep-tree .dep-tree-formui');
    treeUI.empty();

    tree.split('\n').forEach(function(elem, index){
      if(elem) {
        var node = elem.split('\t');
        var spaceafterVal = Boolean(node[9].search('SpaceAfter=No'));
        var rootVal = node[6];
        var deprelVal = node[7];

        var depRel = $(depRelSelect).data('id', index).addClass('inp dep');
        var rootRel = $('<input style="width: 100%;" value="'+rootVal+'">').data('id', index).addClass('inp root');
        var spaceAfter = $('<input tabindex="-1" '+(!spaceafterVal?'checked':'')+' value="SpaceAfter=No" type="checkbox">').data('id', index).addClass('inp spaceafter');

        depRel.val(deprelVal);

        var nodeHTML = $('<div class="row"></div>');
        $('<div class="five wide column">'+node[0]+'\t'+node[1]+'\t</div>').appendTo(nodeHTML);

        var depBox = $('<div class="three wide column"></div>');
        var rootBox = $('<div class="two wide column"></div>');
        depRel.appendTo(depBox);
        depBox.appendTo(nodeHTML);
        rootRel.appendTo(rootBox);
        rootBox.appendTo(nodeHTML);

        $('<div class="four wide column">SpaceAfter=No:</div>').appendTo(nodeHTML);
        var spaceBox = $('<div class="one wide column"></div>');
        spaceAfter.appendTo(spaceBox);
        spaceBox.appendTo(nodeHTML);

        $(nodeHTML).appendTo(treeUI);
      }
    });

    treeUI.find('.inp.root, .inp.dep, .inp.spaceafter').on('change', function(event){
      var trigger = $(this);
      if(trigger.hasClass('dep')) insertIntoTree(trigger.data('id'), 7, trigger.val());
      else if(trigger.hasClass('root')) insertIntoTree(trigger.data('id'), 6, trigger.val());
      else if(trigger.hasClass('spaceafter')) insertIntoTree(trigger.data('id'), 9, trigger.val());
    });
  }
  
  function insertIntoTree(index, featType, val){
    var tree = $('.modal#dep-tree .dep-tree');

    var updTree = [];
    tree.val().split('\n').forEach(function(elem, i){
      if(i == index) {
        var node = elem.split('\t');

        if( featType == 9 && node[featType] != '_')
          node[featType] = '_';
        else
          node[featType] = val || '_';

        updTree.push(node.join('\t'));
      } else updTree.push(elem);
    });

    tree.val(updTree.join('\n'));
  }

  function getCookie(c_name) {
    if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
        c_start = c_start + c_name.length + 1;
        c_end = document.cookie.indexOf(";", c_start);
        if (c_end == -1) c_end = document.cookie.length;
        return unescape(document.cookie.substring(c_start,c_end));
      }
    }
    return '';
  }
  
  $(function () {
    $.ajaxSetup({
      headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    setTimeout(function(){
      
      $(document).delegate('.tab-teaxtarea', 'keydown', function(e) {
        var keyCode = e.keyCode || e.which;

        if (keyCode == 9) {
          e.preventDefault();
          var start = this.selectionStart;
          var end = this.selectionEnd;

          // set textarea value to: text before caret + tab + text after caret
          $(this).val($(this).val().substring(0, start)
                      + "\t"
                      + $(this).val().substring(end));

          // put caret at right position again
          this.selectionStart =
          this.selectionEnd = start + 1;
        }
      });

    }, 500);
  });
 
	$(window).bind("popstate", function( event ) {
		
		core.ajax.query(window.location.pathname);
		
	});
  
  setInterval(core.init, 200);
  setInterval(core.semanticPlugin.init, 200);