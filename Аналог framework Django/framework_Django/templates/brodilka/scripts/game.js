renderer.renderBoard();
//обрабатываем событие если пользователь нажимает клавишу
window.addEventListener('keydown', function(event){
    mover.makeStep(event);
});