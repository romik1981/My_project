let mover = {

    /**
     * Метод проверяет существование ячейки куда может перейти пользователь.
     * @param {{x: number, y: number}} nextPoint координаты ячейки
     * @returns {boolean} если ячейка существует true, иначе false.
     */
    canPlayerMakeStep(nextPoint) {
        return renderer.getSquare(nextPoint) !== null;
    },

    /**
     * Метод выполняет перемещение игрока по полю.
     * @param {KeyboardEvent} event объект события нажатия клавиши.
     * @see https://mzl.la/2zpmGSY
     */
    makeStep(event) {
        let newPosition = this.getNewPosition(event);
        if (this.arePositionsEqual(player, newPosition)) {
            return;
        }
        if (!this.canPlayerMakeStep(newPosition)) {
            return;
        }
        renderer.clearUserPosition();
        player.changePosition(newPosition);
        renderer.renderUserPosition(newPosition)
    },

    /**
     * В зависимости от того какую стрелку нажал пользователь метод возвращает
     * координаты новой ячейки, либо если туда нельзя сделать шаг, то координаты
     * существующей ячейки.
     * @param {KeyboardEvent} event объект события нажатия клавиши.
     * @see https://mzl.la/2DX0Mdp
     * @returns {{x: number, y: number}}
     */
    getNewPosition(event) {
        switch (event.key) {
            case "ArrowUp":
                return {x: player.x, y: player.y - 1};
            case "ArrowDown":
                return {x: player.x, y: player.y + 1};
            case "ArrowLeft":
                return {x: player.x - 1, y: player.y};
            case "ArrowRight":
                return {x: player.x + 1, y: player.y};
            default:
                return {x: player.x, y: player.y};
        }
    },

    /**
     * Метод проверяет совпадают ли координаты двух позиций.
     * @param {{x: number, y: number}} curPos текущая позиция
     * @param {{x: number, y: number}} newPos новая позиция
     * @returns {boolean} если совпадают, то true, иначе false.
     */
    arePositionsEqual(curPos, newPos) {
        return curPos.x == newPos.x && curPos.y == newPos.y; 
    }
};