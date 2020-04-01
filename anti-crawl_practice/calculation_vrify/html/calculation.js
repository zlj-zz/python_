function randNumber(min, max) {
    // 生成合理随机数
    var res = parseInt(Math.random() * (max - min) + min);
    return res;
}
function randColor(min, max) {
    // 随机色方法
    var r = randNumber(min, max); var g = randNumber(min, max); var b = randNumber(min, max);
    var colorRes = `rgb(${r}, ${b}, ${b})`;
    return colorRes;
}
function multMath() {
    // 乘法
    var first = randNumber(1, 20);
    var second = randNumber(5, 15);
    return [first, second, '*'];
}
function additionMath() {
    // 加法
    var first = randNumber(20, 99);
    var second = randNumber(3, 99);
    return [first, second, '+'];
}
function subMath() {
    // 减法
    var first = randNumber(46, 99);
    var second = randNumber(1, 45);
    return [first, second, '-'];
}
var mathesResult = [];  // Canvas 生成的验证码
$(function () {
    var matchesCanvas = document.getElementById('matchesCanvas');
    var cvas = matchesCanvas.getContext('2d');
    // 获取计算题
    var mathList = [multMath(), additionMath(), subMath()];
    var i = (randNumber(0, mathList.length));
    var maths = mathList[i];

    var width = matchesCanvas.width - 20;
    var height = matchesCanvas.height;
    // 绘制背景色
    cvas.fillStyle = '#cdc8b1';
    cvas.fillRect(0, 0, width, height);
    // 绘制计算题
    cvas.fillStyle = '#7f7f7f';
    var fontSize = 26;
    cvas.font = fontSize + 'px Arial';
    cvas.textBaseline = 'middle';
    cvas.fillText(maths[0], 10, 20);
    cvas.fillText(maths[2], 50, 20);
    cvas.fillText(maths[1], 80, 20);
    cvas.fillText('= ?', 120, 20);
    if (i == 0) {
        var result = parseInt(maths[0]) * parseInt(maths[1]);
    } else if (i == 1) {
        var result = parseInt(maths[0]) + parseInt(maths[1]);
    } else {
        var result = parseInt(maths[0]) - parseInt(maths[1]);
    }
    mathesResult.push(result);
    function mathesVerify() {
        // 对比用户输入结果
        var codeInt = parseInt(mathesResult.join(''));
        console.log(codeInt);
        var inputCode = parseInt(document.getElementById('code').value);
        if (inputCode == codeInt) {
            //alert('result:' + inputCode + ', pass!');
            window.location.href = "./index.html"
        } else {
            alert('faild');
        }
    }
    // 绘制干扰信息的方法
    function cvasInterfere(cvas, width, height) {
        // 干扰线
        for (var i = 0; i < 8; i++) {
            cvas.beginPath();
            cvas.moveTo(randNumber(0, width), randNumber(0, height));
            cvas.lineTo(randNumber(0, width), randNumber(0, height));
            cvas.strokeStyle = randColor(180, 220);
            cvas.closePath();
            cvas.stroke();
        }
        // 干扰噪点
        for (var i = 0; i < 80; i++) {
            cvas.beginPath();
            cvas.arc(randNumber(0, width), randNumber(0, height), 1, 0, 2 * Math.PI);
            cvas.closePath();
            cvas.fillStyle = randColor(150, 250);
            cvas.fill();
        }
    }
    // 绘制完成后,添加干扰线和噪点
    cvasInterfere(cvas, width, height);
    var bt = document.getElementById('bt');
    bt.addEventListener('click', function (e) {mathesVerify();});
})

