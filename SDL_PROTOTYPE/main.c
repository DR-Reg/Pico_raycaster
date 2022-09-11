#include <SDL2/SDL.h>
#include <math.h>
#include <time.h>
#include <stdio.h>
#include "level_test.cam"
#define WIDTH 240
#define HEIGHT 135
#define SCALING 3
#define FRAME_POLL 5
#define BLOCK_SIZE 10

#define draw_pixel(x,y) \
    for (int dpx_i= 0; dpx_i < SCALING; dpx_i++) { \
        for (int dpx_j = 0; dpx_j < SCALING; dpx_j++) { \
            SDL_RenderDrawPoint(renderer,(x)*SCALING + dpx_i,(y)*SCALING + dpx_j); \
        }\
    }
#define draw_line(x1,y1,x2,y2) \
    for (int dln_i= 0; dln_i < SCALING; dln_i++) { \
        for (int dln_j = 0; dln_j < SCALING; dln_j++) { \
            SDL_RenderDrawLine(renderer,(x1)*SCALING + dln_i,(y1)*SCALING + dln_j,(x2)*SCALING + dln_i,(y2)*SCALING+dln_j); \
        }\
    }
#define draw_rect(x,y,w,h) \
    for (int drct_i = 0; drct_i < w; drct_i++) {\
        for (int drct_j = 0; drct_j < h; drct_j++) { \
            draw_pixel(x+drct_i,y+drct_j); \
        } \
    }
#define set_color(r,g,b) SDL_SetRenderDrawColor(renderer,r,g,b,255)

typedef struct Player {
    int x,y,dx,dy,v;
    float a, av;
} Player;

unsigned int get_ray(Player p, float rela,SDL_Renderer* renderer);
int main() {
    SDL_Event event;
    SDL_Renderer* renderer;
    SDL_Window* window;
   
    SDL_Init(SDL_INIT_VIDEO);
    SDL_CreateWindowAndRenderer(WIDTH*SCALING, HEIGHT*SCALING, 0, &window, &renderer);

    clock_t tick;
    int frameCount;

    Player p = { 50, 50, 0, 0, 5, 0, 0.4 };
    p.dx = p.v*cos(p.a);p.dy = p.v*sin(p.a);
    p.dx = p.v*cos(p.a);p.dy = p.v*sin(p.a);

    while (1) {
        set_color(255,255,255);
        SDL_RenderClear(renderer);

        // draw player and level in 2D
#ifdef _2D_RAYCAST
        set_color(0,255,0);
        draw_line(p.x,p.y,(p.x+p.dx),(p.y+p.dy));
        set_color(255,0,0);
        draw_rect(p.x-1,p.y-1,3,3); 
        
        for (int i = 0; i < level_test_arr_H; i++) {
            for (int j = 0; j < level_test_arr_W; j++) {
               if (level_test_arr[i*level_test_arr_W+ j]) {
                   unsigned int color = level_test_arr[i*level_test_arr_W+ j];
                   unsigned char r,g,b;
                   r = (color & 0xFF000000) >> 24;
                   g = (color & 0x00FF0000) >> 16;
                   b = (color & 0x0000FF00) >> 8;
                   set_color(r,g,b);
                   draw_rect(j*BLOCK_SIZE,i*BLOCK_SIZE,BLOCK_SIZE-1,BLOCK_SIZE-1);
               }
            }
        }
#endif
        // calculate rays:
        get_ray(p,0,renderer);
        while( SDL_PollEvent( &event ) ){
            if ( event.type == SDL_KEYDOWN){
                switch( event.key.keysym.sym ){
                    case SDLK_UP: p.y += p.dy; p.x += p.dx;break;
                    case SDLK_DOWN: p.y -= p.dy; p.x -= p.dx;break;
                    case SDLK_LEFT: p.a -= p.av; p.dx = p.v*cos(p.a);p.dy = p.v*sin(p.a);break;
                    case SDLK_RIGHT: p.a += p.av; p.dx = p.v*cos(p.a);p.dy = p.v*sin(p.a);break;
                    default:break;
                }
                if (p.a > 2*M_PI) p.a -= 2*M_PI;
                else if (p.a < 0) p.a += 2*M_PI;
            } else if (SDL_PollEvent(&event) && event.type == SDL_QUIT) goto cleanup;
        }

        SDL_RenderPresent(renderer);
        if (frameCount == FRAME_POLL) {
            frameCount = 0;
            double ttaken = (double)(clock()-tick)/CLOCKS_PER_SEC;
            // printf("[FPS:\t%f]\n",FRAME_POLL/ttaken);
            tick = clock();
        }
        frameCount++;
    }
cleanup:
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}

unsigned int get_ray(Player p, float rela, SDL_Renderer* renderer) {

        unsigned int asdf = 16;
        // horizontal:
        int hline = (int)(p.y/BLOCK_SIZE) + (p.a > 0 && p.a < M_PI);
        set_color(255,0,0);
/*#ifdef _2D_RAYCAST
        draw_line(0,hline*BLOCK_SIZE,BLOCK_SIZE * level_test_arr_W,BLOCK_SIZE*hline);
#endif*/
        float tana;
        if (p.a == M_PI/2) tana = -1; // going straight up
        else if (p.a == 3*M_PI/2) tana = 1; // going straight down
        else tana = tan(p.a+rela);
        float dx,dy;
        dy =hline*BLOCK_SIZE - p.y;
        if (tana == 0) goto vertical; 
        else dx = dy/tana;
        set_color(255,255,0);
        float rx, ry;
        rx = p.x+dx;ry=p.y+dy;
        int rxline = (int)((rx)/BLOCK_SIZE) + (p.a > 3 * M_PI_2 || p.a < M_PI_2);
        dy = 1;
        dx = 1/tana;
        int dxline = (int)((dx)/BLOCK_SIZE); 
        int dyline = 2*(p.a > 0 && p.a < M_PI)-1;
        printf("DX/DY: %f,%f\n",dx,dy);
        unsigned int collided = level_test_arr[hline * level_test_arr_W + rxline];
        int dof = 0;
        
        while (!collided && dof < 8) {
            rx += dx;
            ry += dy;
            hline += dyline;
            rxline += dxline;
            collided = level_test_arr[hline * level_test_arr_W + rxline];
            if (hline >= level_test_arr_W || rxline >= level_test_arr_H) break;
            dof++;
        }
        hline += (p.a > 0 && p.a < M_PI);
        
        draw_line(p.x,p.y,rxline*BLOCK_SIZE,hline*BLOCK_SIZE); 
        set_color(255,0,0);
        draw_line(0,hline*BLOCK_SIZE,BLOCK_SIZE * level_test_arr_W,BLOCK_SIZE*hline);
        double dist_to_hline = sqrt(pow(dx,2)+pow(dy,2));

vertical:
        return asdf;
}
