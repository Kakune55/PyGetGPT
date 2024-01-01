// 消息框的js代码

// 获取页面元素
var notification = document.getElementById('notification');
var showNotificationBtn = document.getElementById('showNotificationBtn');
var notificationText = document.getElementById('notificationText');
var progressBarInner = document.getElementById('progressBarInner');

// 显示通知函数
function showNotification(message) {
    // 设置通知文本
    notificationText.innerText = message;
    // 显示通知框
    notification.style.display = 'block';

    // 触发回流(reflow)以启用动画效果
    notification.offsetHeight;

    // 添加显示状态的类，触发过渡效果
    notification.classList.add('show');

    // 启动倒计时
    startCountdown(5); // 延迟时间
}

// 倒计时函数
function startCountdown(duration) {
    var startTime = Date.now();
    var interval = setInterval(function () {
        var currentTime = Date.now();
        var elapsedTime = currentTime - startTime;
        var remainingTime = duration * 1000 - elapsedTime;

        if (remainingTime <= 0) {
            clearInterval(interval);
            closeNotification();
        } else {
            var progressPercent = (remainingTime / (duration * 1000)) * 100;
            updateProgressBar(progressPercent);
        }
    }, 100);
}

// 更新进度条函数
function updateProgressBar(percent) {
    progressBarInner.style.width = percent + '%';
}

// 关闭通知函数
function closeNotification() {
    // 移除显示状态的类，触发过渡效果
    notification.classList.remove('show');
    // 延时等待动画完成后隐藏通知框
    setTimeout(function () {
        notification.style.display = 'none';
        // 重置进度条宽度为 100%
        progressBarInner.style.width = '100%';
    }, 300); // 等待动画完成再隐藏
}