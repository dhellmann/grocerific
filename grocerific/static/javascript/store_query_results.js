var StoreQueryResultsManager = Class.create();
StoreQueryResultsManager.prototype = {
  initialize: function() {
  },
  
  formatItem: function(item) {
	var id = item.getAttributeNode('id').value;
	var desc = item.getAttributeNode('description').value;
	var city = item.getAttributeNode('city').value;
	var icon = '\u2190';

	return DIV({'class':'query_result'}, 
			   A({'title':'Add to my stores', 'class':'action_link',
					 'onclick':'addToList(' + id + ')'}, icon),
			   ' ',
			   A({'title':'Details', 'href':'/item/' + id}, desc),
			   ' ',
			   city
			   );
  },

  registerAJAX: function () {
	ajaxEngine.registerRequest('findStores', '/store/search');
	ajaxEngine.registerAjaxElement('query_results');
	ajaxEngine.registerAjaxElement('query_message');
	ajaxEngine.registerAjaxObject('queryResultsManager', this);
  },

  ajaxUpdate: function(ajaxResponse) {
	var stores = ajaxResponse.getElementsByTagName('store');
	
	if (stores.length > 0) {

	  swapDOM('query_message', DIV({'class':'active_message',
									   'id':'query_message'}, 
								   ''));

	  var formatted_items = map(this.formatItem, stores);
	  swapDOM('query_results', DIV({'class':'query_results',
									   'id':'query_results'},
								   formatted_items));

	}
	else {

	  swapDOM('query_message', DIV({'class':'active_message',
									   'id':'query_message'}, 
								   'No match found'));

	  swapDOM('query_results', DIV({'class':'query_results',
									   'id':'query_results'},
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
  
  findStores: function() {
	var queryString = document.findStore.query.value;
	if (queryString != "") {
	  this.setMessage('loading...');
	  ajaxEngine.sendRequest('findStores', "queryString="+queryString);
	}
  }
};
