class Grafico:
    def _cargas_numpy(self):
        self.cargar_cargas()
        qs  = np.array([float(c.valor) for c in self.cargas.values()], dtype=float)
        xqs = np.array([float(c.x)     for c in self.cargas.values()], dtype=float)
        yqs = np.array([float(c.y)     for c in self.cargas.values()], dtype=float)
        return qs, xqs, yqs

    def graficar_Ex_sobre_eje_x(self):
        """
        E_x(x) sobre y=0: muestra E_x de cada carga y la superposición.
        Rango fijo para simplificar: x ∈ [-10, 10], 1000 puntos.
        """
        qs, xqs, yqs = self._cargas_numpy()

        x = np.linspace(-10.0, 10.0, 1000)
        dx = x[:, None] - xqs[None, :]
        dy = 0.0 - yqs[None, :]
        r  = np.sqrt(dx**2 + dy**2)
        r[r == 0] = np.inf

        Ex_each  = COEFICIENTE_ELECTRICO * qs[None, :] * dx / (r**3)
        Ex_total = Ex_each.sum(axis=1)

        plt.figure(figsize=(9, 5))
        for j in range(qs.size):
            plt.plot(x, Ex_each[:, j], linewidth=1,
                     label=f"E_x carga {j+1} (q={qs[j]}, x={xqs[j]}, y={yqs[j]})")
        plt.plot(x, Ex_total, linewidth=2, label="E_x superposición (todas)")
        plt.axhline(0, linestyle="--", linewidth=0.8)
        plt.xlabel("x [m]")
        plt.ylabel("E_x(x) [N/C]")
        plt.title("Componente E_x sobre el eje x (individuales y superposición)")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo(self):
        qs, xqs, yqs = self._cargas_numpy()

        x = np.linspace(-10.0, 10.0, 200)
        y = np.linspace(-10.0, 10.0, 200)
        X, Y = np.meshgrid(x, y)

        dx = X[..., None] - xqs[None, None, :]
        dy = Y[..., None] - yqs[None, None, :]
        r  = np.sqrt(dx**2 + dy**2)
        r[r == 0] = np.inf

        Ex = (COEFICIENTE_ELECTRICO * qs[None, None, :] * dx / (r**3)).sum(axis=-1)
        Ey = (COEFICIENTE_ELECTRICO * qs[None, None, :] * dy / (r**3)).sum(axis=-1)

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.streamplot(X, Y, Ex, Ey, density=1.2, linewidth=1)

        for j in range(qs.size):
            color = "red" if qs[j] > 0 else "blue"
            ax.scatter([xqs[j]], [yqs[j]], s=60, c=color, edgecolors="k", zorder=3)
            ax.text(xqs[j] + 0.2, yqs[j] + 0.2, f"q{j+1}", fontsize=9)

        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title("Líneas de campo eléctrico (superposición)")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.2)
        plt.tight_layout()
        plt.show()