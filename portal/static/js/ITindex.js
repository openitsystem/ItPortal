/**
 * Created by zy23917 on 2017/7/20.
 */
$(function () {
    var OA_index = {

        dialogObjL: null,
        commonMenu: null,
        otherMenu: null,
        isTouchResultPanel: false,
        sortedMenu: [],
        sortedCommon: [],
        showMenus: [],
        myMenuCode: $('#txtMyMenuCode').val(),
        myMenuId: undefined,
        myMenuList: [],
        myMenuShow: false,
        // approvalCount: {
        //     "Name": '快速审批',
        //     'ImgPath': urlPrefix + 'Images/OAMenu/kuaishushenpicon.png',
        //     'children': []
        // },
        searchList: [],
        commonChange: false,
        index: 0,
        init: function () {
            var self = this;
            // this.fillSwitch();
            // this.versionHandler();
            // this.bindEvent();
            // this.getMenu();
            this.scrollbar = $('.wrapper').scrollbar({
                speed: 32
            });
            $(window).on('resize', function () {
                self.scrollbar.update();
            });
            //左侧收缩
            $('.user-info .user-shrink').click(function (e) {
                var target = e.target;
                if ($(target).closest('#headLink').length || target.id === 'headLink') return;
                $(this).toggleClass('active');
                $(this).next().slideToggle().toggleClass('slide');
                if ($(this).next().hasClass('slide') && $('.exception label').length) {
                    $(this).children('span').addClass('active');
                } else {
                    $(this).children('span').removeClass('active');
                }
            });
        }
    };
    OA_index.init();

// 获取参数
});



