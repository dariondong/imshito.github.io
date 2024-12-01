


btn = document.getElementById('btnpt');

// 默认状态为true,表示开始
// status 是关键字
var status1 = true;
var times;





function load() {
    layui.use(['notify'], function () {
        notify = layui.notify;
        var langtime
        now = new Date(), hour = now.getHours()
        if (hour < 6) { langtime = ("凌晨好！ 每天给自己一个希望，不为明天烦恼，不为昨天叹息，只为今天更美好") }
        else if (hour < 9) { langtime = ("早上好！当第一线光明照彻天际，当第一缕阳光洒满人间，当第一丝清风拂过脸颊，当第一曲铃声悠然响起，那是我的祝福早早来到，愿你拥有一天好心情。") }
        else if (hour < 12) { langtime = ("上午好！希望阳光很暖微风不燥时光不老，你我都好。") }
        else if (hour < 14) { langtime = ("中午好！无论这个世界对你怎样，都请你一如既往的努力、勇敢、充满希望。") }
        else if (hour < 17) { langtime = ("下午好！若岁月静好，那就颐养身心；若时光阴暗，那就多些历练。") }
        else if (hour < 19) { langtime = ("傍晚好！ 不是每个黎明都会有阳光，不是每个彷徨都会有忧伤，不是每个芬芳都会有清香，打开人生的窗，你会发现，曙光仍在") }
        else if (hour < 22) { langtime = ("晚上好！ 梦想无论怎么模糊，它总潜伏在我们心底，使我们的心境永远得不到宁静，直到梦想成为事实。") }
        else { langtime = ("夜里好！") }
        notify.info(langtime, "topRight");
    })
}

function ptc(){
    var str = localStorage.getItem('list')
    var stuArr = str.split(localStorage.getItem('fgf'));
    //  绑定事件,开始定时器,点击就执行书写的变化的函数

    console.log('begin');
    // 如果状态是true就执行开始定时器操作
    if (status1) {
        // 开始定时器,然后调用随机名字数组索引的函数
        times = setInterval(function () {
            // 现在是随机出数组的索引,索引记得是长度减1
            var index = random(0, stuArr.length - 1);
            // 然后把索引对应的值放进名字里
            var name = stuArr[index];
            // 然后把名字放进页面的名字盒子上
            document.getElementById('mz').innerHTML = name;
        }, 30)
        // 当点击的那一刻开始就要对下边的那个span进行变化，变化如下
        document.getElementById('btngroup').innerHTML="\
        <button class=\"layui-btn\" style=\"background-color: brown; \"onclick=\"ptc()\">点击停止</button>";
        // 文字变为停止

        // 状态变为停止
        status1 = false;
    }
    else {
        //清除定时器
        clearInterval(times);
        // 停止以后，也要修改span的状态和文字
        document.getElementById('btngroup').innerHTML=" <button class=\"layui-btn\" id=\"btnpt\" onclick=\"ptc()\" style=\"background-color: rgb(0, 214, 0);\">开始</button><a href=\"./index.html\"><button class=\"layui-btn\" style=\"background-color: rgb(255, 94, 0);\" >刷新摇号盒</button></a>         "
       
        status1 = true;
    }
}
// 随机数的方法
function random(min, max) {
    return Math.round(Math.random() * (max - min) + min)
}