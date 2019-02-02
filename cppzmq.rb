class Cppzmq < Formula
  desc "High-level C++ binding for ZeroMQ"
  homepage "http://czmq.zeromq.org/"
  url "https://github.com/zeromq/cppzmq/archive/v4.3.0.tar.gz"
  sha256 "27d1f56406ba94ee779e639203218820975cf68174f92fbeae0f645df0fcada4"

  head do
    # url "https://github.com/zeromq/cppzmq.git"
    url "https://github.com/zeromq/cppzmq/archive/v4.3.0.tar.gz"
  end

  depends_on "cmake" => :build
  depends_on "zeromq"

  def install
    ENV.cxx11
    system "cmake", "-DCMAKE_INSTALL_PREFIX=#{prefix}", "."
    system "make", "all", "install"
  end

  test do
    system "true"
  end
end
