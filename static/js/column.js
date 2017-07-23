/**
 * Created by RaPoSpectre on 7/23/17.
 */

var page = 2;
var total = 10;
var column = '';

$(function(){
    total = $('#total-page').attr('total');
    column = $('#column-slug').attr('slug');
    $('.article-pagination').remove();
});

new Scrollload({
    container: document.querySelector('.column-content'),
    content: document.querySelector('.article-list'),
    loadMore: function (sl) {
        if (page > total) {
            // 没有数据的时候需要调用noMoreData
            sl.noMoreData();
            return
        }
        $.ajax({
            type: 'GET',
            url: '/column/' + column + '/?page=' + page,
            success: function(data){
                var $n = $(data);
                var items = $n.find("div[class='article-list']").html();
                // contentDom其实就是你的scrollload-content类的dom
                $(sl.contentDom).append(items);

                // 处理完业务逻辑后必须要调用unlock
                sl.unLock();
                page ++;
            },
            error: function(xhr, type){
                // 加载出错，需要执行该方法。这样底部DOM会出现出现异常的样式。
                sl.throwException()
            }
        })

    }

});
