function F(x, y) {
  for(i = 0; i < -x; i += 1) {
    y += 1
  }
  print(y)
  printflush()
}

F(-5, -(5))
