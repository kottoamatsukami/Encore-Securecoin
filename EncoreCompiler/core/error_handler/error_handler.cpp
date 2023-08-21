//
// Created by Enterprice on 8/8/2023.
//
#include "error_handler.h"

#include <iostream>

void ERROR_No_Arguments_Received()
{
    std::cout << "Error: No arguments received" << std::endl;
    exit(1);
}

void ERROR_Could_Not_Open_File()
{
    std::cout << "Error: Could not open the file" << std::endl;
    exit(1);
}