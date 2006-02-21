var QueryResultsManager = Class.create();
QueryResultsManager.prototype = {
  initialize: function() {
  },
  
  formatItem: function(item) {
	var id = item.getAttributeNode('id').value;
	var desc = item.getAttributeNode('description').value;
	var icon = '\u2190';

	return DIV({'class':'query_result'}, 
			   A({'title':'Add to list', 
					 'class':'action_img',
					 'onclick':'addToList(' + id + ')',
					 'alt':icon}, 
				 IMG({'src':'/static/images/icons/arrow_left.png'})
				 ),
			   ' ',
			   A({'title':'Details', 'href':'/item/' + id,
					 'target':'_blank'}, desc)
			   );
  },

  registerAJAX: function () {
	ajaxEngine.registerRequest('findItems', '/item/search');
	ajaxEngine.registerRequest('browseItems', '/item/browse');
	ajaxEngine.registerAjaxElement('query_results');
	ajaxEngine.registerAjaxObject('queryResultsManager', this);
  },

  ajaxUpdate: function(ajaxResponse) {
	var shopping_items = ajaxResponse.getElementsByTagName('shopping_item');
	
	if (shopping_items.length > 0) {

	  swapDOM('query_message', DIV({'class':'active_message',
									   'id':'query_message'}, 
								   ''));

	  var formatted_items = map(this.formatItem, shopping_items);
	  swapDOM('query_results', DIV({'class':'query_results',
									   'id':'query_results'},
								   formatted_items));

	}
	else {

	  swapDOM('query_message', DIV({'class':'active_message',
									   'id':'query_message'}, 
								   'No match found'));

	  swapDOM('query_results', DIV({'id':'query_results'},
								   ''));
	}
  },

  setMessage: function(newMessage) {
	  swapDOM('query_message', DIV({'class':'active_message',
									   'id':'query_message'}, newMessage));
  },

  clearResults: function() {
	  swapDOM('query_results', DIV({'class':'query_results',
									   'id':'query_results'}, ''));
  },
  
  findItems: function() {
	var queryString = document.findItem.query.value;
	if (queryString != "") {
	  this.setMessage('loading...');
	  ajaxEngine.sendRequest('findItems', "queryString="+queryString);
	}
  },

  findItemsByTag: function(tag) {
	this.setMessage('loading...');
	ajaxEngine.sendRequest('findItems', "queryString="+tag);
  },

  browseItems: function(firstLetter) {
	this.setMessage('loading...');
	ajaxEngine.sendRequest('browseItems', "firstLetter="+firstLetter);
  }
};
