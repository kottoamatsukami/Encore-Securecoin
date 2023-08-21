//
// Created by Enterprice on 8/8/2023.
//

#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <iterator>
#include <vector>


class Tokenizer{
    public:
        static void tokenize(std::string str){
            // use std::vector instead, we need to have it in this order
            std::vector<std::pair<std::string, std::string>> v
                    {
                            // Operators
                            {"\\=", "OP_ASSIGN"},
                            {"\\+", "OP_ADD"},
                            {"\\-", "OP_SUB"},
                            {"\\*", "OP_MUL"},
                            {"\\/", "OP_DIV"},
                            {"\\%", "OP_MOD"},

                            {"-?[0-9]+" , "INTEGER"},
                            {"[a-z]+" , "IDENTIFIER"},
                    };

            std::string reg;

            for(auto const& x : v)
                reg += "(" + x.first + ")|"; // parenthesize the submatches

            reg.pop_back();
            std::cout << reg << std::endl;

            std::regex re(reg, std::regex::extended); // std::regex::extended for longest match

            auto words_begin = std::sregex_iterator(str.begin(), str.end(), re);
            auto words_end = std::sregex_iterator();

            for(auto it = words_begin; it != words_end; ++it)
            {
                size_t index = 0;

                for( ; index < it->size(); ++index)
                    if(!it->str(index + 1).empty()) // determine which submatch was matched
                        break;

                std::cout << it->str() << "\t" << v[index].second << std::endl;
            }
        }
};
