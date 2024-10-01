#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

// Функция для генерации ядра Гаусса
vector<vector<double>> generateGaussianKernel(int size, double sigma) { //создает двумерное ядро Гаусса, используя формулу Гаусса. Мы нормализуем ядро, чтобы сумма всех весов была равна 1
    vector<vector<double>> kernel(size, vector<double>(size));
    double sum = 0.0;
    int halfSize = size / 2;

    for (int x = -halfSize; x <= halfSize; ++x) {
        for (int y = -halfSize; y <= halfSize; ++y) {
            kernel[x + halfSize][y + halfSize] = (1 / (2 * M_PI * sigma * sigma)) * exp(-(x * x + y * y) / (2 * sigma * sigma));
            sum += kernel[x + halfSize][y + halfSize];
        }
    }

    // Нормализация ядра
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            kernel[i][j] /= sum;
        }
    }

    return kernel;
}

// Функция для применения гауссовского размытия
vector<vector<double>> gaussianBlur(const vector<vector<int>>& image, int kernelSize, double sigma) {//выполняет свертку изображения с ядром Гаусса. Мы проходим по каждому пикселю изображения и применяем ядро, учитывая пиксели вокруг текущего (с обработкой границ)
    int rows = image.size();
    int cols = image[0].size();
    vector<vector<double>> blurredImage(rows, vector<double>(cols, 0.0));

    auto kernel = generateGaussianKernel(kernelSize, sigma);
    int halfSize = kernelSize / 2;

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            double pixelValue = 0.0;

            // Применение ядра Гаусса
            for (int k = -halfSize; k <= halfSize; ++k) {
                for (int l = -halfSize; l <= halfSize; ++l) {
                    int x = i + k;
                    int y = j + l;

                    // Проверка границ изображения
                    if (x >= 0 && x < rows && y >= 0 && y < cols) {
                        pixelValue += image[x][y] * kernel[k + halfSize][l + halfSize];
                    }
                }
            }

            blurredImage[i][j] = pixelValue; // Устанавливаем новое значение пикселя
        }
    }

    return blurredImage;
}

// Функция для вывода изображения
void printImage(const vector<vector<double>>& image) {
    for (const auto& row : image) {
        for (const auto& pixel : row) {
            cout << (int)pixel << " "; // Приводим к целочисленному значению
        }
        cout << endl;
    }
}

int main() {
    // Пример черно-белого изображения 5x5
    vector<vector<int>> image = {
        {255, 255, 255, 255, 255},
        {255, 0, 0, 0, 255},
        {255, 0, 0, 0, 255},
        {255, 0, 0, 0, 255},
        {255, 255, 255, 255, 255}
    };

    int kernelSize = 3; // Размер ядра размытия
    double sigma = 1.0; // Стандартное отклонение

    // Применяем гауссовское размытие
    vector<vector<double>> blurredImage = gaussianBlur(image, kernelSize, sigma);

    // Выводим размазанное изображение
    cout << "Blurred Image:" << endl;
    printImage(blurredImage);

    return 0;
}
