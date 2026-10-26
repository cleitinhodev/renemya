"""Animações "neon": riscos laranja brilhantes que percorrem bordas e barras.

Feito para ser leve:

- um único ``QTimer`` por janela (:class:`NeonClock`, 30 quadros/s) move todos os riscos;
- cada risco é desenhado numa camada transparente (:class:`NeonOverlay`) por cima do
  widget, que não recebe cliques e não muda o layout;
- a cada quadro só é redesenhado o retângulo pequeno onde o risco estava e onde está agora;
- o relógio para quando as animações estão desligadas, a janela está minimizada,
  escondida ou sem foco, ou quando nenhum risco está visível.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from PySide6.QtCore import QElapsedTimer, QEvent, QObject, QPointF, QRect, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPolygonF,
    QRadialGradient,
    QRegion,
)
from PySide6.QtWidgets import QProgressBar, QWidget

from . import theme

FPS = 30  # divide 60 Hz certinho (ritmo uniforme) e gasta pouco
_STEP = 2.0  # distância (px) entre os pontos amostrados do contorno


def settings_bool(value, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() not in ("false", "0", "no", "off", "")
    return bool(value)


class NeonClock(QObject):
    """Relógio compartilhado pelas animações de uma janela."""

    def __init__(self, parent: QObject | None = None, enabled: bool = True) -> None:
        super().__init__(parent)
        self.t = 0.0  # segundos de animação
        self._enabled = enabled
        self._suspended = False
        self._overlays: list[NeonOverlay] = []
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setInterval(round(1000 / FPS))
        self._timer.timeout.connect(self._on_timeout)
        self._elapsed = QElapsedTimer()
        self._window: QWidget | None = None

    # ------------------------------------------------------------ estado
    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def suspended(self) -> bool:
        return self._suspended

    def is_running(self) -> bool:
        return self._timer.isActive()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)
        for overlay in self.overlays():
            overlay.setVisible(self._enabled)
            overlay.update()
        self._sync()

    def set_suspended(self, suspended: bool) -> None:
        if suspended != self._suspended:
            self._suspended = suspended
            self._sync()

    def overlays(self) -> list[NeonOverlay]:
        alive = []
        for overlay in self._overlays:
            try:
                overlay.objectName()  # dispara RuntimeError se o C++ já foi apagado
            except RuntimeError:
                continue
            alive.append(overlay)
        self._overlays = alive
        return alive

    def register(self, overlay: NeonOverlay) -> None:
        self._overlays.append(overlay)
        overlay.setVisible(self._enabled)
        self._sync()

    def clear(self) -> None:
        """Esquece as camadas atuais (a interface vai ser reconstruída)."""
        self._overlays = []
        self._sync()

    def _sync(self) -> None:
        should_run = self._enabled and not self._suspended and bool(self._overlays)
        if should_run and not self._timer.isActive():
            self._elapsed.restart()
            self._timer.start()
        elif not should_run and self._timer.isActive():
            self._timer.stop()

    # ------------------------------------------------------------ janela
    def watch(self, window: QWidget) -> None:
        """Pausa sozinho quando ``window`` é minimizada, escondida ou perde o foco."""
        self._window = window
        window.installEventFilter(self)
        self.refresh_window_state()

    def refresh_window_state(self) -> None:
        w = self._window
        if w is None:
            return
        try:
            hidden = not w.isVisible() or w.isMinimized()
            inactive = not w.isActiveWindow()
        except RuntimeError:
            return
        self.set_suspended(hidden or inactive)

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if event.type() in (
            QEvent.Type.WindowStateChange,
            QEvent.Type.WindowActivate,
            QEvent.Type.WindowDeactivate,
            QEvent.Type.Show,
            QEvent.Type.Hide,
        ):
            QTimer.singleShot(0, self.refresh_window_state)
        return False

    # ------------------------------------------------------------ quadros
    def advance(self, seconds: float) -> None:
        """Avança a animação (usado pelo timer e pelos testes/capturas de tela)."""
        self.t += seconds
        for overlay in self.overlays():
            overlay.advance()

    def _on_timeout(self) -> None:
        dt = self._elapsed.restart() / 1000.0
        self.advance(min(max(dt, 0.0), 0.1))


@dataclass(frozen=True)
class NeonStyle:
    """Como o risco anda e brilha."""

    mode: str = "border"  # "border" (contorna o widget) ou "bar" (faixa na barra de progresso)
    speed: float = 140.0  # px/s
    trail: float = 90.0  # comprimento do rastro (px)
    streaks: int = 1  # quantos riscos ao mesmo tempo
    radius: float = 12.0  # cantos arredondados do contorno
    inset: float = 1.0  # distância da borda do widget
    top: float = 0.0  # deslocamento do topo (ex.: título do QGroupBox)
    width: float = 2.0  # espessura do núcleo
    glow: float = 7.0  # espessura do brilho
    strength: float = 1.0  # intensidade (0..1)
    additive: bool = False  # soma a luz (clareia demais sobre o azul; desligado por padrão)
    phase: float = 0.0  # atraso inicial (fração da volta)
    color: str = ""  # cor do risco ("" = laranja neon do tema)


class NeonOverlay(QWidget):
    """Camada transparente sobre ``target`` que desenha o(s) risco(s) neon."""

    def __init__(self, target: QWidget, clock: NeonClock, style: NeonStyle) -> None:
        super().__init__(target)
        self.target = target
        self.clock = clock
        self.style_ = style
        self.active = True  # dá para desligar um risco sem remover a camada
        self.setObjectName("NeonOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAutoFillBackground(False)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._points: list[QPointF] = []
        self._length = 0.0
        self._dirty: list[QRect] = []
        target.installEventFilter(self)
        self.setGeometry(target.rect())
        self._rebuild_path()
        self.raise_()
        clock.register(self)

    # ------------------------------------------------------------ geometria
    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self.target and event.type() == QEvent.Type.Resize:
            self.setGeometry(self.target.rect())
            self._rebuild_path()
            self.raise_()
        elif obj is self.target and event.type() == QEvent.Type.ChildAdded:
            self.raise_()
        return False

    def frame_rect(self) -> QRectF:
        s = self.style_
        r = QRectF(self.rect())
        return r.adjusted(s.inset, s.inset + s.top, -s.inset, -s.inset)

    def _rebuild_path(self) -> None:
        self._points = []
        self._length = 0.0
        if self.style_.mode != "border":
            return
        rect = self.frame_rect()
        if rect.width() < 4 or rect.height() < 4:
            return
        radius = min(self.style_.radius, rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        length = path.length()
        count = max(int(length / _STEP), 8)
        self._points = [
            path.pointAtPercent(path.percentAtLength(i * length / count)) for i in range(count)
        ]
        self._length = length

    # ------------------------------------------------------------ animação
    def is_live(self) -> bool:
        """O risco está aparecendo agora?"""
        if not (self.active and self.clock.enabled and self.target.isVisible()):
            return False
        if self.style_.mode == "bar":
            return isinstance(self.target, QProgressBar) and self.target.isEnabled()
        return self.target.isEnabled()

    def advance(self) -> None:
        rects = self.dirty_rects() if self.is_live() else []
        region = QRegion()
        for rect in self._dirty + rects:  # onde o risco estava + onde está agora
            region += rect
        self._dirty = rects
        if not region.isEmpty():
            self.update(region)

    def _heads(self) -> list[float]:
        s = self.style_
        if self._length <= 0:
            return []
        base = self.clock.t * s.speed + s.phase * self._length
        return [(base + k * self._length / s.streaks) % self._length for k in range(s.streaks)]

    def _trail_points(self, head: float) -> list[QPointF]:
        n = len(self._points)
        step = self._length / n
        h = int(head / step)
        count = max(int(self.style_.trail / step), 2)
        return [self._points[(h - count + i) % n] for i in range(count + 1)]

    def dirty_rects(self) -> list[QRect]:
        """Retângulos (um por risco) que precisam ser redesenhados neste quadro."""
        pad = math.ceil(self.style_.glow + 4)
        if self.style_.mode == "bar":
            return [self._chunk_rect().toAlignedRect().adjusted(-1, -1, 1, 1)]
        rects = []
        for head in self._heads():
            pts = self._trail_points(head)
            xs = [p.x() for p in pts]
            ys = [p.y() for p in pts]
            r = QRectF(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
            rects.append(r.toAlignedRect().adjusted(-pad, -pad, pad, pad).intersected(self.rect()))
        return rects

    # ------------------------------------------------------------ pintura
    def paintEvent(self, event) -> None:  # noqa: N802
        if not self.is_live():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.style_.additive:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Plus)
        if self.style_.mode == "bar":
            self._paint_bar(painter)
        else:
            for head in self._heads():
                self._paint_streak(painter, self._trail_points(head))
        painter.end()

    def _paint_streak(self, painter: QPainter, pts: list[QPointF]) -> None:
        s = self.style_
        neon = QColor(s.color or theme.current().neon)
        hot = QColor("#ffe7c7")
        pieces = 16
        per = max((len(pts) - 1) // pieces, 1)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        layers = ((s.glow, 0.16), (s.glow * 0.45, 0.32), (s.width, 0.95))
        for layer, (width, alpha) in enumerate(layers):
            for i in range(0, len(pts) - 1, per):
                frac = min((i + per) / (len(pts) - 1), 1.0)  # 0 = cauda, 1 = cabeça
                ease = frac**1.6
                color = QColor(neon)
                if layer == 2 and frac > 0.7:  # núcleo mais claro perto da cabeça
                    mix = (frac - 0.7) / 0.3 * 0.8
                    color = QColor(
                        round(neon.red() + (hot.red() - neon.red()) * mix),
                        round(neon.green() + (hot.green() - neon.green()) * mix),
                        round(neon.blue() + (hot.blue() - neon.blue()) * mix),
                    )
                color.setAlphaF(max(0.0, min(1.0, alpha * ease * s.strength)))
                # pontas retas: os pedaços se encostam sem sobrepor (sem "contas" no risco)
                pen = QPen(color, max(width * (0.5 + 0.5 * frac), 0.8))
                pen.setCapStyle(Qt.PenCapStyle.FlatCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                painter.drawPolyline(QPolygonF(pts[i : i + per + 1]))
        # brilho suave na cabeça
        head = pts[-1]
        radius = s.glow * 0.75
        grad = QRadialGradient(head, radius)
        c0, c1, c2 = QColor(hot), QColor(neon), QColor(neon)
        c0.setAlphaF(0.7 * s.strength)
        c1.setAlphaF(0.35 * s.strength)
        c2.setAlphaF(0.0)
        grad.setColorAt(0.0, c0)
        grad.setColorAt(0.4, c1)
        grad.setColorAt(1.0, c2)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(head, radius, radius)

    def _chunk_rect(self) -> QRectF:
        bar = self.target
        if not isinstance(bar, QProgressBar):
            return QRectF()
        span = max(bar.maximum() - bar.minimum(), 1)
        frac = (bar.value() - bar.minimum()) / span
        inner = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        inner.setWidth(max(inner.width() * frac, min(inner.width(), 24.0)))
        return inner

    def _paint_bar(self, painter: QPainter) -> None:
        s = self.style_
        chunk = self._chunk_rect()
        if chunk.width() <= 0:
            return
        neon = QColor(theme.current().neon)
        band = max(s.trail, 30.0)
        travel = chunk.width() + band
        x = (self.clock.t * s.speed) % travel - band + chunk.left()
        clip = QPainterPath()
        clip.addRoundedRect(chunk, s.radius, s.radius)
        painter.setClipPath(clip)
        # brilho alaranjado que passeia pela parte preenchida
        grad = QLinearGradient(x, 0, x + band, 0)
        edge = QColor(neon)
        edge.setAlphaF(0.0)
        mid = QColor("#ffd2a3")  # laranja claro: sobre o azul não "suja" a cor
        mid.setAlphaF(0.38 * s.strength)
        grad.setColorAt(0.0, edge)
        grad.setColorAt(0.75, mid)
        grad.setColorAt(1.0, edge)
        painter.fillRect(QRectF(x, chunk.top(), band, chunk.height()), QBrush(grad))
        # filete fino e brilhante embaixo, como um risco de luz
        line = QLinearGradient(x, 0, x + band, 0)
        bright = QColor("#ffe7c7")
        bright.setAlphaF(0.95 * s.strength)
        line.setColorAt(0.0, edge)
        line.setColorAt(0.8, neon)
        line.setColorAt(0.97, bright)
        line.setColorAt(1.0, edge)
        y = chunk.bottom() - s.width
        painter.fillRect(QRectF(x, y, band, s.width), QBrush(line))


def install(target: QWidget, clock: NeonClock, **style) -> NeonOverlay:
    """Atalho: ``install(botao, relogio, speed=120, trail=70)``."""
    return NeonOverlay(target, clock, NeonStyle(**style))


__all__ = ["FPS", "NeonClock", "NeonOverlay", "NeonStyle", "install", "settings_bool"]
