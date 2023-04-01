
function mainload() {

    layer.msg('加载中')
    adminkey = localStorage.getItem("adminkey");
    if (adminkey == null) { firsttime() }
    L1N = localStorage.getItem("L1N");
    L1 = localStorage.getItem("L1");
    L2N = localStorage.getItem("L2N");
    L2 = localStorage.getItem("L2");
    L3N = localStorage.getItem("L3N");
    L3 = localStorage.getItem("L3");


    layer.msg('完成')

}

function firsttime() {
    localStorage.setItem("L1",['李白','杜甫','韩愈','柳宗元','欧阳修','苏洵','苏轼','苏辙','王安石','曾巩','陶渊明','辛弃疾','李贺','陆游'])
    layer.msg('初始化')
    Notification.requestPermission(function (status) {

        layer.msg("你是第一次使用吧！")

        newadminkey = prompt("建新管理员密码：")
        if (newadminkey == null || newadminkey == "") {
            alert("不行哦，要有密码")
            firsttime()
        }
        else {
            adminkey = newadminkey
            localStorage.setItem("adminkey", newadminkey)
            layer.msg("设置成功")
        }
    });
}

function openset() {
    if (adminkey == prompt("管理员密码")) {
        document.getElementById('settext').value=L1
        layer.open({
            area: ['500px', '300px'],
            type: 1,
            content: $('#setpage'),
            cancel: function () { document.getElementById('setpage').style.display = 'none' }
        });
    }
    else {
        layer.msg("管理员密码错误")
    }
}


// console.log(stuArr);

// 获取页面中节点对象
var names = document.getElementById('uname')
var btn = document.getElementById('yao')

// 默认状态为true,表示开始
// status 是关键字
var status1 = true;
var times;

function random(min, max) {
    return Math.round(Math.random() * (max - min) + min)
}
//  绑定事件,开始定时器,点击就执行书写的变化的函数
function c() {
    
    var cL1 =L1.split(',');
    // 现在是随机出数组的索引,索引记得是长度减1
    var index = random(0, cL1.length - 1);
    // 然后把索引对应的值放进名字里
    var name = String(cL1[index]);
    // 然后把名字放进页面的名字盒子上
    document.getElementById('uname').innerHTML = name
}



function setsava(){
    L1 =document.getElementById('settext').value
    localStorage.setItem("L1",L1)
    layer.msg("保存"+L1)
}
