$(function () {
    var tracks = document.getElementById('tracks'),
        sliderblock = document.getElementById('sliderblock'),
        slidertips = document.getElementById('slidertips'),
        bt = document.getElementById('bt');
});
// 滑块宽度
var sliderblockWidth = $('#sliderblock').width();
// 滑轨长度
var tracksWidth = $('#tracks').width();
var mousemove = false; // mousedown 状态
sliderblock.addEventListener('mousedown', function (e) {
    // 监听 mousedown 事件, 记录滑块起始位置
    mousemove = true;
    startCoordinateX = e.clientX;
});
var distanceCoordinateX = 0; // 滑块起始位置
tracks.addEventListener('mousemove', function (e) {
    // 监听鼠标移动
    if (mousemove) { // 鼠标点击滑块后才跟踪移动
        distanceCoordinateX = e.clientX - startCoordinateX; // 滑块当前位置
        if (distanceCoordinateX > tracksWidth - sliderblockWidth) {
            // 通过限制滑块位置,避免滑块右移出轨
            distanceCoordinateX = tracksWidth - sliderblockWidth;
        } else if (distanceCoordinateX < 0) {
            // 避免左移出轨
            distanceCoordinateX = 0;
        }
        // 根据移动距离显示话快位置
        sliderblock.style.left = distanceCoordinateX + 'px';
    }
});
sliderblock.addEventListener('mouseup', function (e) {
    // 鼠标松开视为完成滑动, 记录滑块当前位置并调用验证方法
    var endCoordinateX = e.clientX;
    verifySliderResult(endCoordinateX);
});
function verifySliderResult(endCoordinateX) { // 滑动验证结果
    mousemove = false; // 此时鼠标松开,防止跟随继续滑动
    // 允许存在误差
    if (Math.abs(endCoordinateX - startCoordinateX - tracksWidth) < sliderblockWidth + 3) {
        // 成功后的样式
        sliderblock.style.color = '#666';
        sliderblock.style.fontsize = '28px';
        sliderblock.style.background = '#fff';
        sliderblock.innerHTML = '√';
        slidertips.style['visibility'] = 'visible';
        console.log('successful');
    } else {
        // 若失败,复位
        distanceCoordinateX = 0;
        slidertips.style.left = 0;
        console.log('faild');
    }
};
bt.addEventListener('click', function (e) {
    if (slidertips.style['visibility'] == 'visible') {
        window.location.href = "./index.html";
        console.log('1');
    } else {
        $("text").show();

    }
});

