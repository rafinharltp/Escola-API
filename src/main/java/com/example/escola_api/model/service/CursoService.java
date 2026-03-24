package com.example.escola_api.model.service;

import com.example.escola_api.model.entity.Curso;
import com.example.escola_api.model.repository.CursoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CursoService {

    private final CursoRepository cursoRepository;

    public CursoService(CursoRepository cursoRepository) {
        this.cursoRepository = cursoRepository;
    }

    public Curso criarCurso(Curso curso) {
        return cursoRepository.save(curso);
    }

    public List<Curso> listarCursos() {
        return cursoRepository.findAll();
    }

    public Optional<Curso> buscarPorId(Long id) {
        return cursoRepository.findById(id);
    }

    public Curso atualizarCurso(Long id, Curso dadosAtualizados) {
        return cursoRepository.findById(id)
                .map(curso -> {
                    curso.setNome(dadosAtualizados.getNome());
                    curso.setDescricao(dadosAtualizados.getDescricao());
                    curso.setCargaHoraria(dadosAtualizados.getCargaHoraria());
                    return cursoRepository.save(curso);
                })
                .orElseThrow(() -> new RuntimeException("Curso não encontrado"));
    }

    public void deletarCurso(Long id) {
        cursoRepository.deleteById(id);
    }
}

