#include<pybind11/pybind11.h>
#include<pybind11/numpy.h>
#include<fstream>
#include<iostream>

namespace py = pybind11;

/*
https://blog.csdn.net/u013701860/article/details/86313781
https://blog.csdn.net/u011021773/article/details/83188012
*/

py::array_t<float> calcMul(py::array_t<float>& input1, py::array_t<float>& input2) {

    // read inputs arrays buffer_info
    py::buffer_info buf1 = input1.request();
    py::buffer_info buf2 = input2.request();

    if (buf1.size != buf2.size)
    {
        throw std::runtime_error("Input shapes must match");
    }

    // allocate the output buffer
    py::array_t<double> result = py::array_t<double>(buf1.size);



}

class Matrix
{
public:
    Matrix() {};
    Matrix(int rows, int cols) {
        this->m_rows = rows;
        this->m_cols = cols;
        m_data = new float[rows*cols];
    }
    ~Matrix() {};

private:
    int m_rows;
    int m_cols;
    float* m_data;

public:
    float* data() { return m_data; };
    int rows() { return m_rows; };
    int cols() { return m_cols; };

};




void save_2d_numpy_array(py::array_t<float, py::array::c_style> a, std::string file_name) {

    std::ofstream out;
    out.open(file_name, std::ios::out);
    std::cout << a.ndim() << std::endl;
    for (int i = 0; i < a.ndim(); i++)
    {
        std::cout << a.shape()[i] << std::endl;
    }
    for (int i = 0; i < a.shape()[0]; i++)
    {
        for (int j = 0; j < a.shape()[1]; j++)
        {
            if (j == a.shape()[1]-1)
            {
                //访问读取,索引 numpy.ndarray 中的元素
                out << a.at(i, j)<< std::endl;
            }
            else {
                out << a.at(i, j) << " ";
            }
        }
    }

}

//
//py::array_t<unsigned char, py::array::c_style> rgb_to_gray(py::array_t<unsigned char, py::array::c_style>& a) {
//
//  py::array_t<unsigned char, py::array::c_style> dst = py::array_t<unsigned char, py::array::c_style>(a.shape()[0] * a.shape()[1]);
//  //指针访问numpy矩阵
//  unsigned char* p = (unsigned char*)dst.ptr();
//
//  for (int i = 0; i < a.shape()[0]; i++)
//  {
//      for (int j = 0; j < a.shape()[1]; j++)
//      {
//          auto var = a.data(i, j);
//          auto R = var[0];
//          auto G = var[1];
//          auto B = var[2];
//
//          //RGB to gray
//          auto gray = (R * 30 + G * 59 + B * 11 + 50) / 100;
//
//          std::cout << static_cast<int>(R) << " " << static_cast<int>(G) << " " << static_cast<int>(B)<< std::endl;
//
//          //p[i*a.shape()[1] + j] = static_cast<unsigned char>(gray);
//
//      }
//  }
//}

PYBIND11_MODULE(numpy_demo, m) {

    m.doc() = "Simple numpy demo";

    py::class_<Matrix>(m,"Matrix",py::buffer_protocol())
        .def_buffer([](Matrix& mm)->py::buffer_info {
        return py::buffer_info(
            mm.data(),          //Pointer to buffer, 数据指针
            sizeof(float),      //Size of one scalar, 每个元素大小(byte)
            py::format_descriptor<float>::format(), //python struct-style foramt descriptor
            2,                      //Number of dims, 维度
            {mm.rows(), mm.cols()}, //strides (in bytes)
            {sizeof(float) * mm.cols(),sizeof(float)}
        );
    });

    m.def("save_2d_numpy_array", &save_2d_numpy_array);
    //m.def("rgb_to_gray", &rgb_to_gray);
}
