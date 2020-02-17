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

import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.util.Arrays;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;
import java.util.function.Supplier;

import static org.junit.Assert.assertEquals;

public class RuleReaderTest {

    private File file;
    private List<File> subFiles;
    private RuleReader reader;
    private Supplier<String> lines;
    private Supplier<String> lines2;
    private Rules rules;

    @Before
    public void setup() {
        // given
        file = new File("directory/main.rule");
        rules = new Rules();
        subFiles = new LinkedList<>();
        reader = new RuleReader() {
            @Override
            public void load(Rules rules, File file) {
                subFiles.add(file);

                processLines(rules, file, lines2);
            }
        };
    }
    
    private Supplier<String> load(String... input) {
        Deque<String> list = new LinkedList<>(Arrays.asList(input));
        return () -> {
            if (list.isEmpty()) {
                return null;
            }
            return list.removeFirst();
        };
    }

    @Test
    public void shouldNoRules_whenEmptyFile() {
        // given
        lines = load("");

        // when
        reader.processLines(rules, file, lines);

        // then
        assertEquals("[]", rules.toString());

    }

    @Test
    public void shouldSeveralRules_whenSingleFile() {
        // given
        lines = load(
                "...",
                "♥☺.",
                "...",
                "RIGHT",
                "",
                "...",
                ".☺♥",
                "...",
                "LEFT",
                "",
                ".♥.",
                ".☺.",
                "...",
                "DOWN",
                "",
                ".☼.",
                "☼☺.",
                ".♥.",
                "RIGHT",
                "",
                "...",
                ".☺.",
                ".♥.",
                "UP");

        // when
        reader.processLines(rules, file, lines);

        // then
        assertEquals(
                "[[...♥☺.... > RIGHT], " +
                "[....☺♥... > LEFT], " +
                "[.♥..☺.... > DOWN], " +
                "[.☼.☼☺..♥. > RIGHT], " +
                "[....☺..♥. > UP]]", rules.toString());
    }

    @Test
    public void shouldLoadRules_whenRuleDirective() {
        // given
        lines = load(
                ".☼.",
                ".☺.",
                "...",
                "DOWN",
                "",
                "........",
                "........",
                "........",
                "☺",
                "........",
                "........",
                "........",
                "RULE right",
                "",
                "...",
                "☼☺☼",
                ".#.",
                "UP");
        
        lines2 = load(".☼.",
                ".☺ ",
                ".☼.",
                "RIGHT",
                "",
                ".☼.",
                ".☺ ",
                ".#.",
                "RIGHT",
                "",
                ".#.",
                ".☺ ",
                ".☼.",
                "RIGHT",
                "",
                ".#.",
                ".☺ ",
                ".#.",
                "RIGHT");

        // when
        reader.processLines(rules, file, lines);

        // then
        assertEquals(
                "[[.☼..☺.... > DOWN], " +
                "[........................☺........................ > [" +
                    "[.☼..☺ .☼. > RIGHT], " +
                    "[.☼..☺ .#. > RIGHT], " +
                    "[.#..☺ .☼. > RIGHT], " +
                    "[.#..☺ .#. > RIGHT]]" +
                "], " +
                "[...☼☺☼.#. > UP]]", rules.toString());
    }
    
}
