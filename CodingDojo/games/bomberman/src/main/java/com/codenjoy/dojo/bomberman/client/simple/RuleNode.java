package com.codenjoy.dojo.bomberman.client.simple;

/*-
 * #%L
 * Codenjoy - it's a dojo-like platform from developers to developers.
 * %%
 * Copyright (C) 2018 - 2020 Codenjoy
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

import com.codenjoy.dojo.bomberman.client.Board;
import com.codenjoy.dojo.services.Direction;

public class RuleNode implements Rule {

    private String pattern;
    private Rules rules;

    public RuleNode(String pattern, Rules rules) {
        this.pattern = pattern;
        this.rules = rules;
    }

    @Override
    public String pattern() {
        return pattern;
    }

    @Override
    public Direction direction(Board board) {
        return rules.process(board);
    }

    @Override
    public String toString() {
        return String.format("[%s > %s]", pattern, rules.toString());
    }
}
