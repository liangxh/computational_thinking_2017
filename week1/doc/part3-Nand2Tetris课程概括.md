# Nand2Tetris课程概括

## 来源

* 学校: MIT
* 讲师: Noam Nisan, Shimon Schocken

## 背景

* 计算机科学专业的学生并不了解计算机的底层实现原理
* 越来越少的学生选修编译相关的课程
* 很多计算机结构课程的教学内容过于详细而且枯燥
* 并没有激起从无到有的这种兴奋感

## 目标

* 指导学生和自学者了解从电路起了解现今计算机的软硬件架构
* 让学生透过完成12节课的作业充分了解计算机的抽象实现

## 课程特色

* 模块化的课程内容和作业允许学生根据个人需要单独学习需要的部分
* 作业中使用的仿真软件可以在各种操作系统上运行
* 完成课程所需要的所有知识均包含在课程当中，适合本科或以上学历的计算机专业学生
* 非专业学生建议先掌握基本的编程的知识
* 仅从抽象层次讲解计算机软硬件架构，不考虑具体的硬件实现
    * 正如现今软硬件工程师在设计计算机时同样不考虑具体硬件实现

## 课程大纲

* 第一部分: 布尔逻辑与电子电路
    * 对应课程
        * Lecture 1 - Boolean Logic 布尔逻辑: 讲解布尔逻辑与门电路
        * Lecture 2 - Boolean Arithmetic 布尔运算: 讲解基于布尔逻辑实现数字运算
        * Lecture 3 - Sequential Logic 时序逻辑: 介绍时钟和Flip-flop，以及基于其实现的存储部件
    * 对应作业
        * Project 1: 基于And, Or, Not等门编写各加法器和ALU的.hdl文件
        * Project 2: 编写各种存储部件的.hdl文件
        * Project 3: 基于Nand门编写各逻辑元件的.hdl文件

* 第二部分: 机器语言
    * 对应章节
        * Lecture 4 - Machine Language 机器语言: 讲解机器语言与编码
    * 对应作业
        * Project 4: 利用汇编语言实现简单功能 (汇编语言经由CPUEmulator转换为二进制机器语言.hack)
* 第三部分: 汇编语言
    * 对应章节
        * Lecture 5 - Computer Architecture 计算机架构: 讲解计算机的抽象架构
        * Lecture 6 - Assembler 汇编器: 讲解汇编语言以及到机器语言的转换
    * 对应作业
        * Project 5: 编写CPU，Memory等部件，并实现加法等程序的.hdl文件
        * Project 6: 运行由Jack语言编写后汇编成的代码
* 第四部分: 虚拟机
    * 对应章节
        * Lecture 7 - Virtual Machine I 虚拟机: 讲解VM中栈的push, pop操作
        * Lecture 8 - Virtual Machine II 虚拟机: 讲解基于VM中实现的函数调用
    *　对应作业
        * Project 7: 利用VM Emulator运行给定程序了解栈操作
        * Project 8: 利用VM Emulator运行给定程序了解函数调用
* 第五部分: 高级语言
    * 对应章节
        * Lecture 9: High Level Language 高级语言
        * Lecture 10: Compiler I 编译器
        * Lecture 11: Compiler II 编译器
    * 对应作业
        * Project 9: (?)
        * Project 10: (?)
        * Project 11: (?)
    
* 第六部分: 操作系统与软件应用
    * 对应章节
        * Lecture 12: OS
    * 对应作业
        * Project 12: 基于Jack实现要求的功能
        * Project 13: 鼓励学生基于现有框架开发自己的应用
## 其他

* 所有课程素材可以在官网上免费下载
* 课程衍生的书可以在Amazon上购买
* 大部分学员反馈Nand2Tetris参与过最好的课程

## 参考材料

* Nand2Tetris Official Site [link](http://www.nand2tetris.org)