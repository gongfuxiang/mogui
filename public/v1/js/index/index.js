/**
 * 左侧菜单
 */
var nav_left = new Vue({
    el: '#nav-left',

    // 数据
    data : {
        // 左侧菜单样式
        content_style : {}
    },

    // 操作方法
    methods: {
        handleOpen(key, keyPath) {
            console.log('open', key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log('close', key, keyPath);
        }
    }
});
/**
 * 内容区域
 */
var content = new Vue({
    el: '#content',

    // 数据
    data : {
        // iframe样式
        content_style : {}
    },

    // 初始化区块
    created : function()
    {
        // 注册鼠标滚动事件
        window.addEventListener('resize', this.content_style_change);

        // 初始化iframe窗口
        this.content_style_change();
    },

    // 函数列表
    methods : {
        /**
         * [content_style_change iframe样式操作函数]
         * @author   Devil
         * @blog     http://gong.gg/
         * @version  0.0.1
         * @datetime 2017-07-28T18:03:36+0800
         */
        content_style_change : function()
        {
            // iframe宽高样式初始化
            this.content_style = {
                width : (window.innerWidth-180)+'px',
                height : (window.innerHeight-145)+'px'
            }
console.log(window.innerWidth-180, window.innerHeight-145);
            // 更新左侧菜单高度
            nav_left.content_style = {height : (window.innerHeight-130)+'px'};
        }
    }
});