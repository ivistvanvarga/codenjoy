package com.codenjoy.dojo.reversi.model;

/*-
 * #%L
 * Codenjoy - it's a dojo-like platform from developers to developers.
 * %%
 * Copyright (C) 2016 Codenjoy
 * %%
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public
 * License along with this program.  If not, see
 * <http://www.gnu.org/licenses/gpl-3.0.html>.
 * #L%
 */


import com.codenjoy.dojo.reversi.model.items.Chip;
import com.codenjoy.dojo.services.Point;
import com.codenjoy.dojo.services.multiplayer.GameField;

public interface Field extends GameField<Player> {

    boolean isFree(int x, int y);

    void setChip(boolean color, int x, int y);

    Chip getChip(Point point);

    int size();

    boolean getFreeColor();

    boolean currentColor();

    boolean stop();
}
