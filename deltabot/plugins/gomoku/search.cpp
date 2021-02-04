#pragma GCC optimize(3)
#include <iostream>
#include <iomanip>
#include <thread>
#define SEARCH_DEPTH 2 //模拟?轮
#define INF 900000000

using namespace std;

void extendSimAera(int x, int y);
int evaluation(); //评估函数入口
int getAnalysisingList(int x, int y); //评估子函数
int analysisPattern(); //评估子函数
int simulation(int round, int alpha, int beta); //模拟函数入口

int chessboard[15][15] = {}; //主棋盘
int simulating_aera[25][25] = {};  //设定需要模拟的区域
int best_x, best_y;

extern "C"{
    int cSearch(int *raw_input);
    int cEstimate(int *raw_input);
}

//棋形列表(16个棋形)
static char pattern_list[16][8] = {
    {'*', '*', '*', 'O', 'O', 'O', 'O', 'O'},
    {'*', '*', '+', 'O', 'O', 'O', 'O', '+'},
    {'*', '*', '+', 'O', 'O', 'O', '+', '+'},
    {'*', '+', '+', 'O', 'O', 'O', '+', '*'},
    {'*', '*', '+', 'O', 'O', '+', 'O', '+'},
    {'*', '*', '+', 'O', '+', 'O', 'O', '+'},
    {'*', '*', '*', 'O', 'O', 'O', 'O', '+'},
    {'*', '*', '+', 'O', 'O', 'O', 'O', '*'},
    {'*', '*', '*', 'O', 'O', '+', 'O', 'O'},
    {'*', '*', '*', 'O', '+', 'O', 'O', 'O'},
    {'*', '*', '*', 'O', 'O', 'O', '+', 'O'},
    {'*', '+', '+', 'O', 'O', '+', '+', '*'},
    {'*', '+', '+', 'O', '+', 'O', '+', '*'},
    {'*', '*', '+', 'O', '+', 'O', '+', '+'},
    {'+', '+', '+', 'O', '+', '+', '*', '*'},
    {'*', '+', '+', 'O', '+', '+', '+', '*'},
};

//如果不是本棋型则跳转（优化加速）
static int jump_list[16][8] = {
    {14, 3, 2, 16, 5, 4, 2, 1},       //0
    {14, 3, 6, 16, 5, 4, 2, 3},       //1
    {14, 3, 6, 16, 5, 4, 4, 3},       //2
    {14, 4, 6, 16, 5, 4, 4, 4},       //3
    {14, 11, 6, 16, 5, 5, 10, 7},     //4
    {14, 11, 6, 16, 6, 8, 10, 7},     //5
    {14, 11, 7, 16, 9, 8, 10, 7},     //6
    {14, 11, 8, 16, 9, 8, 10, 8},     //7
    {14, 11, 11, 16, 9, 9, 10, 11},   //8
    {14, 11, 11, 16, 10, 11, 10, 11}, //9
    {14, 11, 11, 16, 12, 11, 14, 11}, //10
    {14, 13, 16, 16, 12, 12, 14, 13}, //11
    {14, 13, 16, 16, 16, 14, 14, 13}, //12
    {14, 14, 16, 16, 16, 14, 14, 14}, //13
    {15, 16, 16, 16, 16, 16, 15, 16}, //14
    {16, 16, 16, 16, 16, 16, 16, 16}, //15
};

//棋形所对应的分数
static int pattern_score[16] = {INF, 4320, 720, 720, 720, 720, 720, 720, 720, 720, 720, 120, 120, 120, 20, 20};


// void display_chessboard()//输出棋盘
// {
//     char output;
//     for (int y = 14; y >= 0; y--)
//     {
//         cout << setw(2) << y + 1 << " ";
//         for (int x = 0; x < 15; x++)
//         {
//             if (chessboard[x][y] == 0)
//                 output = '.';
//             if (chessboard[x][y] == 1)
//                 output = 'X';
//             if (chessboard[x][y] == 2)
//                 output = 'O';
//             cout << output << "  ";
//         }
//         cout << endl;
//     }
//     cout << "   1  2  3  4  5  6  7  8  9  10 11 12 13 14 15" << endl;
// }



// int main()
// {
//     int x, y;
//     int a[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
//     while (1)
//     {
//     int ret = py_interface(a);
//     chessboard[ret/15][ret%15] = 2;
//     a[ret] = 2;
//     display_chessboard();
//     cout << ret/15+1 << " " << ret%15+1 << endl;
//     // cout << best_x << " " << best_y << endl;
//     cin >> x >> y;
//     a[(x-1)*15+y-1] = 1;
//     }
// }


int cSearch(int *raw_input)
{
    // 用于对接python
    for(int i=0; i<15; i++)
    {
        for(int j=0; j<15; j++)
        {
            chessboard[i][j] = raw_input[i*15+j];
            if (!chessboard[i][j])
                extendSimAera(i, j);
        }
    }

    simulation(1, -INF, INF);
    return best_x*15 + best_y;
}

int cEstimate(int *raw_input)
{
    // 用于对接python
    for(int i=0; i<15; i++)
    {
        for(int j=0; j<15; j++)
        {
            chessboard[i][j] = raw_input[i*15+j];
            if (!chessboard[i][j])
                extendSimAera(i, j);
        }
    }

    return evaluation();
}


void extendSimAera(int x, int y)
{
    x += 5;
    y += 5; // FIXME: 防止越界报错，使用时记得也+5
    simulating_aera[x + 1][y] = simulating_aera[x + 2][y] = simulating_aera[x + 3][y] = 1;
    simulating_aera[x - 1][y] = simulating_aera[x - 2][y] = simulating_aera[x - 3][y] = 1;
    simulating_aera[x][y + 1] = simulating_aera[x][y + 2] = simulating_aera[x][y + 3] = 1;
    simulating_aera[x][y - 1] = simulating_aera[x][y - 2] = simulating_aera[x][y - 3] = 1;
    simulating_aera[x + 1][y + 1] = simulating_aera[x + 2][y + 2] = simulating_aera[x + 3][y + 3] = 1;
    simulating_aera[x - 1][y - 1] = simulating_aera[x - 2][y - 2] = simulating_aera[x - 3][y - 3] = 1;
    simulating_aera[x - 1][y + 1] = simulating_aera[x - 2][y + 2] = simulating_aera[x - 3][y + 3] = 1;
    simulating_aera[x + 1][y - 1] = simulating_aera[x + 2][y - 2] = simulating_aera[x + 3][y - 3] = 1;
}


int analysising_list[8];
int evaluation()//评估函数入口
{
    //评估函数（包括 evaluation, getAnalysisingList, analysisPattern）的入口
    //获取跟踪棋子位置
    int score = 0;  //score(分数)
    for (int y = 0; y < 15; y++)
    {
        for (int x = 0; x < 15; x++)
        {
            if (chessboard[x][y] != 0)//当当前棋子位置不是空位的时候
            {
                score += getAnalysisingList(x, y);  //将棋子位置输入子函数，并合并每个被跟踪棋子分数
                //getAnalysisingList返回当前分数
            }
        }
    }
    return score;//返回总分数
}


int getAnalysisingList(int x, int y)//评估子函数
//用于获取被跟踪棋子周围4个方向的棋子，将每个方向跟踪棋子前3个棋子和后4个棋子（加本身共8个元素）写入数组 analysising_list[8]
//输入被跟踪棋子的 x, y，返回被跟踪棋子的分数
{
    int score = 0;
    int pos_x, pos_y;

    //横向
    for (int i = 0; i < 8; i++)
    {
        pos_x = x - 3 + i;
        if (pos_x < 0 || pos_x > 14)
        {
            analysising_list[i] = -1;
        }
        else
        {
            analysising_list[i] = chessboard[pos_x][y];
        }
    }
    score += analysisPattern();  //调用子函数分析获取的 analysising_list[8]，并合并每一数组分数



    //纵向
    for (int i = 0; i < 8; i++)
    {
        pos_y = y - 3 + i;
        if (pos_y < 0 || pos_y > 14)
        {
            analysising_list[i] = -1;
        }
        else
        {
            analysising_list[i] = chessboard[x][pos_y];
        }
    }
    score += analysisPattern();



    //左下到右上
    for (int i = 0; i < 8; i++)
    {
        pos_x = x - 3 + i;
        pos_y = y - 3 + i;
        if (pos_y < 0 || pos_y > 14 || pos_x < 0 || pos_x > 14)
        {
            analysising_list[i] = -1;
        }
        else
        {
            analysising_list[i] = chessboard[pos_x][pos_y];
        }
    }
    score += analysisPattern();



    //左上到右下
    for (int i = 0; i < 8; i++)
    {
        pos_x = x - 3 + i;
        pos_y = y + 3 - i;
        if (pos_y < 0 || pos_y > 14 || pos_x < 0 || pos_x > 14)
        {
            analysising_list[i] = -1;
        }
        else
        {
            analysising_list[i] = chessboard[pos_x][pos_y];
        }
    }
    score += analysisPattern();

    return score;
}



int analysisPattern()//评估子函数
//用于识别棋形，评估核心函数
//输入 数组 analysising_list[8]，返回 本数组分数

/*
    analysising_list[0][1][2] 为被跟踪棋子前三个棋子
    analysising_list[3] 为被跟踪棋子
    analysising_list[4][5][6][7] 为被跟踪棋子后三个棋子

    analysising_list[i] = -1(边界外) / 0(无棋子) / 1(玩家棋子) / 2(Ai棋子)
*/

{
    char comparator;
    for (int i = 0; i < 16; i++)  //16个棋形
    {
        for (int k = 0; k < 9; k++)  //加上分数共9项
        {
            if (k == 8) //判断是否为在读取分数项
            {
                if (analysising_list[3] == 2)
                    return pattern_score[i];   //Ai棋子
                else
                    return -pattern_score[i];  //玩家棋子
            }
            else
            {
                comparator = pattern_list[i][k];

                if (comparator == '+' && analysising_list[k] != 0)  //判断空位
                {
                    i = jump_list[i][k] - 1;
                    break;
                }

                else if (comparator == 'O' && analysising_list[k] != analysising_list[3])  //判断棋子
                {
                    i = jump_list[i][k] - 1;
                    break;
                }

                //'*'为空位，不必判断
            }
        }
    }
    return 0;
}



int simulation(int round, int alpha, int beta) //模拟函数
//TODO: 注意：必须使用1 (1为开始轮数)

//返回最佳下棋点
{
    if (round > SEARCH_DEPTH) //检测是否模拟完毕最后一轮，调用评估
    {
        return evaluation();
    }
    else
    {
        int chess_type = round % 2 + 1;  //round为奇数时模拟Ai(max)下子，偶数数时模拟玩家(min)下子

        for (int y = 0; y < 15; y++)
        {

            for (int x = 0; x < 15; x++)
            {
                if (alpha >= beta)
                    return alpha;  //剪枝，返回任意一不影响母节点的值（alpha到beta之间的任意值）
                
                if (simulating_aera[x + 5][y + 5] == 0)  //定义时+5防止越界，此处调用时也+5
                    continue;

                if (chessboard[x][y] == 0) //空位判断
                {
                    chessboard[x][y] = chess_type;
                    int score = simulation(round + 1, alpha, beta);
                    chessboard[x][y] = 0;

                    if (chess_type == 2) //奇数时模拟Ai取max
                    {
                        if (score > alpha)
                        {
                            alpha = score;
                            best_x = x; //如果是第一轮需返回的最好下棋位置x
                            best_y = y; //如果是第一轮需返回的最好下棋位置y
                        }
                    }
                    else //if (chess_type == 1)  偶数时模拟玩家取min
                    {
                        if (score < beta)
                        {
                            beta = score;
                        }
                    }

                }

            }
        }

        if (chess_type == 2)
            return alpha;
        else //if (chess_type == 1)
            return beta;



    }


}
